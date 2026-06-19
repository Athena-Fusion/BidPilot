"""RequirementAgent - 资格要求提取Agent"""
import re
from backend.agents.base_agent import BaseAgent, AgentContext, AgentResult
from backend.models.schemas import RequirementItem


class RequirementAgent(BaseAgent):
    name = "RequirementAgent"
    description = "资格要求提取与分析Agent"

    async def mock_run(self, context: AgentContext) -> AgentResult:
        text = context.tender_text
        requirements = []

        # 提取资格条件段落
        qual_section = self._extract_section(text, "资格")

        # 按行分析资格要求
        lines = qual_section.split("\n") if qual_section else text.split("\n")

        # 高风险关键词
        high_risk_kw = ["无效投标", "废标", "实质性要求", "★", "不得", "不接受"]
        medium_risk_kw = ["必须", "须", "业绩", "资质", "证书", "认证", "社保", "纳税"]

        for line in lines:
            line = line.strip()
            if not line or len(line) < 5:
                continue
            # 只处理看起来像要求的行
            if any(kw in line for kw in ["具有", "须", "应当", "不得", "不接受", "须具有", "提供", "参加"]):
                req_type = self._classify_requirement(line)
                risk_level = "low"
                mandatory = False

                for kw in high_risk_kw:
                    if kw in line:
                        risk_level = "high"
                        mandatory = True
                        break
                if risk_level != "high":
                    for kw in medium_risk_kw:
                        if kw in line:
                            risk_level = "medium"
                            mandatory = True
                            break

                suggestion = self._get_suggestion(line, req_type)

                requirements.append(RequirementItem(
                    requirement=line[:200],
                    type=req_type,
                    mandatory=mandatory,
                    risk_level=risk_level,
                    suggestion=suggestion
                ))

        # 如果没有提取到，添加默认项
        if not requirements:
            requirements = self._default_requirements(text)

        return AgentResult(
            agent=self.name,
            output=[r.model_dump() for r in requirements],
            summary=f"提取{len(requirements)}项资格要求，其中高风险{sum(1 for r in requirements if r.risk_level=='high')}项",
            references=["招标文件第二章"]
        )

    def _extract_section(self, text: str, keyword: str) -> str:
        """提取包含关键词的章节"""
        pattern = rf'第[一二三四五六七八九十]+章.*{keyword}.*?(?=第[一二三四五六七八九十]+章|$)'
        m = re.search(pattern, text, re.DOTALL)
        return m.group(0) if m else ""

    def _classify_requirement(self, line: str) -> str:
        if "业绩" in line:
            return "业绩要求"
        elif "资质" in line or "认证" in line or "CMMI" in line or "ISO" in line:
            return "资质要求"
        elif "人员" in line or "项目经理" in line or "PMP" in line:
            return "人员要求"
        elif "联合体" in line:
            return "联合体要求"
        elif "社保" in line or "纳税" in line or "税收" in line:
            return "财务要求"
        else:
            return "基本资格"

    def _get_suggestion(self, line: str, req_type: str) -> str:
        if req_type == "业绩要求":
            return "需准备合同关键页、中标通知书或验收证明"
        elif req_type == "资质要求":
            return "需确认企业是否具备相关资质认证"
        elif req_type == "人员要求":
            return "需确认项目人员资质证书有效性"
        elif req_type == "联合体要求":
            return "注意本项目是否允许联合体投标"
        else:
            return "需人工确认是否满足"

    def _default_requirements(self, text: str) -> list[RequirementItem]:
        """根据项目类型生成默认资格要求"""
        if "智慧园区" in text:
            return [
                RequirementItem(requirement="CMMI3级及以上认证", type="资质要求", mandatory=True, risk_level="high", suggestion="需确认企业CMMI认证等级"),
                RequirementItem(requirement="近三年至少2个类似信息化平台建设项目业绩", type="业绩要求", mandatory=True, risk_level="high", suggestion="需准备合同关键页、中标通知书或验收证明"),
                RequirementItem(requirement="项目经理PMP认证或信息系统项目管理师证书", type="人员要求", mandatory=True, risk_level="medium", suggestion="需确认项目经理资质证书有效性"),
                RequirementItem(requirement="ISO 27001信息安全管理体系认证", type="资质要求", mandatory=True, risk_level="medium", suggestion="需确认ISO 27001认证有效性"),
            ]
        elif "数据中台" in text or "数据治理" in text:
            return [
                RequirementItem(requirement="CMMI3级及以上认证", type="资质要求", mandatory=True, risk_level="high", suggestion="需确认企业CMMI认证等级"),
                RequirementItem(requirement="近三年至少3个数据治理或数据中台相关项目业绩", type="业绩要求", mandatory=True, risk_level="high", suggestion="需准备合同关键页、中标通知书或验收证明"),
                RequirementItem(requirement="项目团队至少2人具有数据治理相关认证", type="人员要求", mandatory=True, risk_level="medium", suggestion="需确认DAMA CDMP等认证有效性"),
                RequirementItem(requirement="ISO 27001信息安全管理体系认证", type="资质要求", mandatory=True, risk_level="medium", suggestion="需确认ISO 27001认证有效性"),
            ]
        else:
            return [
                RequirementItem(requirement="CMMI2级及以上认证", type="资质要求", mandatory=True, risk_level="medium", suggestion="需确认企业CMMI认证等级"),
                RequirementItem(requirement="近三年至少2个政务服务相关项目业绩", type="业绩要求", mandatory=True, risk_level="high", suggestion="需准备合同关键页、中标通知书或验收证明"),
                RequirementItem(requirement="项目经理3年以上电子政务项目管理经验", type="人员要求", mandatory=True, risk_level="medium", suggestion="需确认项目经理经验"),
            ]

    def _build_prompt(self, context: AgentContext) -> str:
        return f"""请从以下招标文件中提取所有资格要求，标注类型（业绩/资质/人员/财务）、是否强制、风险等级和建议。

招标文件内容：
{context.tender_text[:3000]}"""

    def _build_system_prompt(self) -> str:
        return "你是投标资格分析专家。请准确提取资格要求，标注风险等级，不确定内容标注'需人工确认'。"
