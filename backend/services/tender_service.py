"""TenderService - 招标分析编排服务"""
import time
import uuid
import logging
from backend.agents.base_agent import AgentContext
from backend.models.schemas import AgentTrace
from backend.agents.tender_parser_agent import TenderParserAgent
from backend.agents.requirement_agent import RequirementAgent
from backend.agents.scoring_agent import ScoringAgent
from backend.agents.risk_agent import RiskAgent
from backend.agents.strategy_agent import StrategyAgent
from backend.agents.solution_agent import SolutionAgent
from backend.agents.business_agent import BusinessAgent
from backend.agents.response_table_agent import ResponseTableAgent
from backend.agents.compliance_agent import ComplianceAgent
from backend.agents.report_agent import ReportAgent
from backend.services.document_loader import DocumentLoader
from backend.services.knowledge_service import KnowledgeService
from backend.services.export_service import ExportService
from backend.models.schemas import AnalysisResult, BasicInfo, RequirementItem, ScoringResult, StrategyResult, SolutionResult, BusinessResponse, ResponseTables, ComplianceResult, Reports
from backend.config import MOCK_MODE

logger = logging.getLogger(__name__)


class TenderService:
    """招标分析编排核心服务"""

    def __init__(self):
        self.parser = TenderParserAgent()
        self.requirement = RequirementAgent()
        self.scoring = ScoringAgent()
        self.risk = RiskAgent()
        self.strategy = StrategyAgent()
        self.solution = SolutionAgent()
        self.business = BusinessAgent()
        self.response_table = ResponseTableAgent()
        self.compliance = ComplianceAgent()
        self.report = ReportAgent()

    async def analyze(self, tender_id: str, tender_text: str = "") -> AnalysisResult:
        """执行完整分析流程"""
        task_id = f"analysis_{uuid.uuid4().hex[:8]}"
        trace = []
        previous_outputs = {}

        # 1. 加载招标文件
        if not tender_text:
            try:
                tender_text = await DocumentLoader.load_from_sample(tender_id)
            except FileNotFoundError as exc:
                raise ValueError(str(exc)) from exc

        if not tender_text:
            return AnalysisResult(task_id=task_id, tender_id=tender_id, mode="mock" if MOCK_MODE else "llm")

        # 2. 知识库检索
        knowledge_refs = await KnowledgeService.search(tender_text)

        # 3. 依次执行各Agent
        ctx = AgentContext(tender_id=tender_id, tender_text=tender_text, knowledge_refs=[kr.model_dump() for kr in knowledge_refs])

        # TenderParserAgent
        t0 = time.time()
        r = await self.parser.run(ctx)
        basic_info = BasicInfo(**(r.output or {}))
        ctx.basic_info = r.output or {}
        previous_outputs["basic_info"] = r.output or {}
        trace.append(AgentTrace(agent=r.agent, status="completed", summary=r.summary, duration_ms=int((time.time()-t0)*1000), references=r.references))

        # RequirementAgent
        t0 = time.time()
        r = await self.requirement.run(ctx)
        requirements_data = r.output or []
        ctx.requirements = requirements_data
        previous_outputs["requirements"] = requirements_data
        trace.append(AgentTrace(agent=r.agent, status="completed", summary=r.summary, duration_ms=int((time.time()-t0)*1000), references=r.references))

        # ScoringAgent
        t0 = time.time()
        r = await self.scoring.run(ctx)
        scoring = ScoringResult(**(r.output or {}))
        ctx.scoring = r.output or {}
        previous_outputs["scoring"] = r.output or {}
        trace.append(AgentTrace(agent=r.agent, status="completed", summary=r.summary, duration_ms=int((time.time()-t0)*1000), references=r.references))

        # RiskAgent
        t0 = time.time()
        r = await self.risk.run(ctx)
        risks_data = r.output or []
        ctx.risks = risks_data
        previous_outputs["risks"] = risks_data
        trace.append(AgentTrace(agent=r.agent, status="completed", summary=r.summary, duration_ms=int((time.time()-t0)*1000), references=r.references))

        # StrategyAgent
        t0 = time.time()
        r = await self.strategy.run(ctx)
        strategy = StrategyResult(**(r.output or {}))
        previous_outputs["strategy"] = r.output or {}
        trace.append(AgentTrace(agent=r.agent, status="completed", summary=r.summary, duration_ms=int((time.time()-t0)*1000), references=r.references))

        # SolutionAgent
        t0 = time.time()
        r = await self.solution.run(ctx)
        solution = SolutionResult(**(r.output or {}))
        previous_outputs["solution"] = r.output or {}
        trace.append(AgentTrace(agent=r.agent, status="completed", summary=r.summary, duration_ms=int((time.time()-t0)*1000), references=r.references))

        # BusinessAgent
        t0 = time.time()
        r = await self.business.run(ctx)
        business_response = BusinessResponse(**(r.output or {}))
        previous_outputs["business_response"] = r.output or {}
        trace.append(AgentTrace(agent=r.agent, status="completed", summary=r.summary, duration_ms=int((time.time()-t0)*1000), references=r.references))

        # ResponseTableAgent
        t0 = time.time()
        r = await self.response_table.run(ctx)
        response_tables = ResponseTables(**(r.output or {}))
        previous_outputs["response_tables"] = r.output or {}
        trace.append(AgentTrace(agent=r.agent, status="completed", summary=r.summary, duration_ms=int((time.time()-t0)*1000), references=r.references))

        # ComplianceAgent
        t0 = time.time()
        r = await self.compliance.run(ctx)
        compliance = ComplianceResult(**(r.output or {}))
        previous_outputs["compliance"] = r.output or {}
        trace.append(AgentTrace(agent=r.agent, status="completed", summary=r.summary, duration_ms=int((time.time()-t0)*1000), references=r.references))

        # ReportAgent
        t0 = time.time()
        ctx.previous_outputs = previous_outputs
        r = await self.report.run(ctx)
        reports = Reports(**(r.output or {}))
        previous_outputs["reports"] = r.output or {}
        trace.append(AgentTrace(agent=r.agent, status="completed", summary=r.summary, duration_ms=int((time.time()-t0)*1000), references=r.references))

        # 导出报告
        exported_files = []
        try:
            exported_files = await ExportService.export_reports(task_id, reports.model_dump())
        except Exception as e:
            logger.error(f"导出报告失败: {e}")

        result = AnalysisResult(
            task_id=task_id,
            tender_id=tender_id,
            tender_name=basic_info.project_name,
            mode="mock" if MOCK_MODE else "llm",
            basic_info=basic_info,
            requirements=[RequirementItem(**d) for d in requirements_data if isinstance(d, dict)],
            scoring=scoring,
            risks=risks_data,
            strategy=strategy,
            solution=solution,
            business_response=business_response,
            response_tables=response_tables,
            compliance=compliance,
            reports=reports,
            agent_trace=trace,
            knowledge_refs=[kr.model_dump() for kr in knowledge_refs],
        )

        # Store result for later retrieval
        self._last_result = result

        return result

    def get_last_result(self) -> AnalysisResult | None:
        return getattr(self, '_last_result', None)


# 全局服务实例
tender_service = TenderService()
