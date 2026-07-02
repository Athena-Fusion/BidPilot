"""RiskAgent - 废标风险识别Agent"""
import re
from backend.agents.base_agent import BaseAgent, AgentContext, AgentResult
from backend.models.schemas import RiskItem


class RiskAgent(BaseAgent):
    name = "RiskAgent"
    description = "废标风险识别Agent"

    async def mock_run(self, context: AgentContext) -> AgentResult:
        text = context.tender_text
        risks = []

        # 价格废标风险
        if "超过采购预算" in text or "超过预算" in text:
            budget_m = re.search(r'预算[：:]\s*人民币?(\d+)万元', text)
            budget = budget_m.group(1) + "万元" if budget_m else "需人工确认"
            risks.append(RiskItem(
                risk=f"投标报价不得超过采购预算{budget}",
                risk_type="价格废标风险",
                severity="high",
                evidence="招标文件：投标报价超过采购预算的，按无效投标处理",
                action=f"报价策略必须控制在{budget}以内，并预留价格评分空间"
            ))

        # 保证金风险
        bond_m = re.search(r'投标保证金[：:]\s*人民币?(\d+\.?\d*万?元)', text)
        if bond_m:
            risks.append(RiskItem(
                risk=f"须按规定交纳投标保证金{bond_m.group(1)}",
                risk_type="格式废标风险",
                severity="high",
                evidence="招标文件：未按规定交纳投标保证金的，按无效投标处理",
                action=f"确保在截止时间前交纳保证金{bond_m.group(1)}，并确认到账"
            ))

        # 签章风险
        if "签字盖章" in text or "加盖公章" in text:
            risks.append(RiskItem(
                risk="投标文件须按规定签字盖章",
                risk_type="格式废标风险",
                severity="high",
                evidence="招标文件：投标文件未按规定签字盖章的，按无效投标处理",
                action="制作签章检查清单，逐页确认盖章和签字"
            ))

        # ★号参数风险
        star_count = text.count("★")
        if star_count > 0:
            risks.append(RiskItem(
                risk=f"存在{star_count}处★号实质性技术参数，必须逐条响应",
                risk_type="技术废标风险",
                severity="high",
                evidence="招标文件：带★号条款为实质性要求，未响应按无效投标处理",
                action="技术方案和响应表必须逐条覆盖所有★号参数，不得遗漏"
            ))

        # 联合体风险
        if "不接受联合体" in text:
            risks.append(RiskItem(
                risk="本项目不接受联合体投标",
                risk_type="资格废标风险",
                severity="medium",
                evidence="招标文件：本项目不接受联合体投标",
                action="确认以独立投标人身份参与投标"
            ))

        # 业绩要求风险
        if "业绩" in text and ("至少" in text or "不少于" in text):
            risks.append(RiskItem(
                risk="存在类似项目业绩要求",
                risk_type="商务风险",
                severity="medium",
                evidence="招标文件：须提供类似项目业绩证明",
                action="提前整理业绩合同关键页、中标通知书和验收证明"
            ))

        # 国产化风险
        if "国产" in text or "信创" in text:
            risks.append(RiskItem(
                risk="存在国产化适配要求",
                risk_type="技术风险",
                severity="medium",
                evidence="招标文件：须适配国产CPU、操作系统、数据库等",
                action="确认产品国产化适配情况，准备适配证明材料"
            ))

        # 等保风险
        if "等保" in text:
            level_m = re.search(r'等保(二级|三级)', text)
            level = level_m.group(1) if level_m else "需人工确认"
            risks.append(RiskItem(
                risk=f"须满足等保{level}要求",
                risk_type="合规风险",
                severity="medium",
                evidence=f"招标文件：须满足等保{level}要求",
                action=f"确认系统等保{level}测评方案，预留测评时间和费用"
            ))

        # 数据安全风险
        if "数据安全" in text or "加密" in text:
            risks.append(RiskItem(
                risk="存在数据安全和加密要求",
                risk_type="技术风险",
                severity="medium",
                evidence="招标文件：敏感数据须加密存储，加密算法须符合国家密码管理要求",
                action="确认支持国密算法（SM2/SM3/SM4），准备加密方案"
            ))

        # PDF格式风险
        if "PDF格式" in text:
            risks.append(RiskItem(
                risk="投标文件须为PDF格式",
                risk_type="格式废标风险",
                severity="low",
                evidence="招标文件：投标文件须为PDF格式",
                action="确保所有投标文件转换为PDF格式并检查可读性"
            ))

        # 服务周期风险
        period_m = re.search(r'(\d+)日.*完成建设', text)
        if period_m:
            risks.append(RiskItem(
                risk=f"建设周期要求{period_m.group(1)}日内完成",
                risk_type="商务风险",
                severity="low",
                evidence=f"招标文件：合同签订后{period_m.group(1)}日内完成建设",
                action="评估项目团队产能，确保可在规定工期内交付"
            ))

        high_count = sum(1 for r in risks if r.severity == "high")
        medium_count = sum(1 for r in risks if r.severity == "medium")

        return AgentResult(
            agent=self.name,
            output=[r.model_dump() for r in risks],
            summary=f"识别{len(risks)}项风险，其中高风险{high_count}项、中风险{medium_count}项",
            references=["invalid_bid_risk_rules.md", "招标文件第六章"]
        )

    async def llm_run(self, context: AgentContext, llm_output: str) -> AgentResult:
        try:
            from backend.utils.json_parser import extract_json
            data = extract_json(llm_output)
            if not isinstance(data, list):
                if isinstance(data, dict):
                    for k, v in data.items():
                        if isinstance(v, list):
                            data = v
                            break
                if not isinstance(data, list):
                    raise ValueError("解析结果不是列表格式")
            
            risks = []
            for item in data:
                if not isinstance(item, dict):
                    continue
                risk_text = item.get("risk", item.get("风险描述", ""))
                if not risk_text:
                    continue
                risk_type = item.get("risk_type", item.get("风险类型", "其他风险"))
                severity = item.get("severity", item.get("严重程度", "medium")).lower()
                if severity not in {"high", "medium", "low"}:
                    severity = "medium"
                evidence = item.get("evidence", item.get("依据", "需人工确认"))
                action = item.get("action", item.get("建议措施", "需人工确认"))
                
                risks.append(RiskItem(
                    risk=risk_text,
                    risk_type=risk_type,
                    severity=severity,
                    evidence=evidence,
                    action=action
                ))
                
            if not risks:
                raise ValueError("未提取到任何有效的风险项")
                
            high_count = sum(1 for r in risks if r.severity == "high")
            medium_count = sum(1 for r in risks if r.severity == "medium")
            
            return AgentResult(
                agent=self.name,
                output=[r.model_dump() for r in risks],
                summary=f"识别{len(risks)}项风险（LLM），其中高风险{high_count}项、中风险{medium_count}项",
                references=["招标文件第六章"]
            )
        except Exception as e:
            self.logger.warning(f"LLM 风险识别解析失败: {e}，将退回到规则模式提取")
            return await self.mock_run(context)

    def _build_prompt(self, context: AgentContext) -> str:
        return f"""请从以下招标文件中识别所有废标风险和商务风险，标注风险类型、严重程度、证据和处理建议。

请以 JSON 数组格式返回，每个对象包含字段：risk, risk_type, severity, evidence, action。

招标文件内容：
{context.tender_text[:3000]}"""

    def _build_system_prompt(self) -> str:
        return "你是投标风险识别专家。请识别废标风险、商务风险和技术风险，不确定内容标注'需人工确认'。不生成围标、串标、控标建议。"
