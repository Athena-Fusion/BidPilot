"""StrategyAgent - 投标策略生成Agent"""
from backend.agents.base_agent import BaseAgent, AgentContext, AgentResult
from backend.models.schemas import StrategyResult


class StrategyAgent(BaseAgent):
    name = "StrategyAgent"
    description = "投标策略生成Agent"

    async def mock_run(self, context: AgentContext) -> AgentResult:
        text = context.tender_text
        risks = context.risks if context.risks else []
        scoring = context.scoring if context.scoring else {}
        strategy = StrategyResult()

        high_risks = [r for r in risks if isinstance(r, dict) and r.get("severity") == "high"]
        high_risk_count = len(high_risks)

        if high_risk_count <= 2:
            strategy.recommendation = "建议参与"
        elif high_risk_count <= 4:
            strategy.recommendation = "谨慎参与"
        else:
            strategy.recommendation = "不建议参与，除非补齐关键材料"

        tech_score = scoring.get("technical_score", 0) if isinstance(scoring, dict) else 0
        if tech_score >= 60:
            strategy.win_assessment = "技术分占比高，若技术方案扎实则有较好胜算。需重点关注高权重评分项和★号实质性要求。"
        elif tech_score >= 50:
            strategy.win_assessment = "技术分占比较高，技术方案质量是关键。同时需确保商务和价格分不落后。"
        else:
            strategy.win_assessment = "评分结构较为均衡，需全面提升各部分得分。"

        strategy.score_strategy = self._build_score_strategy(text)
        strategy.price_suggestion = self._build_price_suggestion(text)
        strategy.material_checklist = self._build_material_checklist(text)
        strategy.management_summary = self._build_management_summary(text, strategy, high_risk_count)

        return AgentResult(
            agent=self.name,
            output=strategy.model_dump(),
            summary=f"策略建议：{strategy.recommendation}",
            references=["common_scoring_rules.md", "invalid_bid_risk_rules.md"]
        )

    def _build_score_strategy(self, text: str) -> list[str]:
        if "智慧园区" in text:
            return [
                "技术方案重点覆盖：总体架构(10分)、设备接入(10分)、国产化适配(10分)三个高权重项",
                "★号参数必须逐条完全响应：设备协议200种、并发500用户、国产化全适配、数据安全全实现、日志180天",
                "商务得分关键：准备2个以上类似业绩(8分)、项目经理PMP(3分)、CMMI4级(2分)",
                "价格分采用低价优先法，报价需合理控制"
            ]
        elif "数据中台" in text or "数据治理" in text:
            return [
                "技术方案重点覆盖：数据治理(15分)、数据交换(12分)、总体架构(12分)、数据质量(10分)四个高权重项",
                "★号参数必须逐条响应：元数据管理、质量规则、数据源10种、REST API、等保三级",
                "商务得分关键：准备3个以上数据中台业绩(6分)、DAMA认证人员(5分)",
                "数据治理方案需体现体系化方法论"
            ]
        else:
            return [
                "技术方案重点覆盖：移动端适配(12分)、流程优化(12分)、平台升级(10分)三个高权重项",
                "★号参数必须逐条响应：移动端全适配、流程优化20个、时限压缩30%",
                "商务得分关键：售后服务(6分)、业绩(8分)、培训天数(3分)",
                "流程优化方案需有量化承诺和实现路径"
            ]

    def _build_price_suggestion(self, text: str) -> str:
        for kw in ["480万元", "800万元", "350万元"]:
            if kw in text:
                return f"报价须控制在{kw}以内。建议参考同类项目中标价，预留5-10%的价格评分空间，避免低价恶性竞争。报价策略需合规，不得涉及围标、串标、控标。"
        return "报价须控制在预算以内，预留价格评分空间。报价策略需合规，不得涉及围标、串标、控标。"

    def _build_material_checklist(self, text: str) -> list[str]:
        checklist = ["营业执照副本复印件", "财务审计报告（近两年）", "依法缴纳税收和社保证明", "无重大违法记录声明"]
        if "CMMI" in text:
            checklist.append("CMMI认证证书复印件")
        if "ISO" in text:
            checklist.append("ISO 27001认证证书复印件")
        if "业绩" in text:
            checklist.append("类似项目业绩合同关键页（首页、金额页、签字页、验收页）")
        if "PMP" in text or "项目经理" in text:
            checklist.append("项目经理资质证书和社保证明")
        if "保证金" in text:
            checklist.append("投标保证金交纳凭证")
        checklist.append("投标文件盖章检查清单")
        return checklist

    def _build_management_summary(self, text: str, strategy: StrategyResult, high_risk_count: int) -> str:
        if "智慧园区" in text:
            pt = "智慧园区"
        elif "数据中台" in text:
            pt = "数据中台"
        elif "政务服务" in text:
            pt = "政务服务"
        else:
            pt = "信息化项目"
        return f"本项目为{pt}类政企信息化项目，建议{strategy.recommendation}。识别出{high_risk_count}项高风险项，需重点关注废标条款和★号实质性要求。技术分占比最高，是得分关键。所有结论仅作为投标辅助参考，最终决策需由投标负责人确认。"

    def _build_prompt(self, context: AgentContext) -> str:
        return f"基于招标文件分析结果生成投标策略建议：{context.tender_text[:2000]}"

    def _build_system_prompt(self) -> str:
        return "你是投标策略专家。不生成围标、串标、控标或不正当竞争建议。所有建议仅作为辅助参考。"
