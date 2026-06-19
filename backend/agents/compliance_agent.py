"""ComplianceAgent - 合规审查Agent"""
from backend.agents.base_agent import BaseAgent, AgentContext, AgentResult
from backend.models.schemas import ComplianceResult, ComplianceIssue


class ComplianceAgent(BaseAgent):
    name = "ComplianceAgent"
    description = "合规审查Agent"

    async def mock_run(self, context: AgentContext) -> AgentResult:
        text = context.tender_text
        risks = context.risks if context.risks else []
        compliance = ComplianceResult()

        critical = []
        warnings = []
        manual_items = []
        suggestions = []

        # 检查★号参数覆盖
        star_count = text.count("★")
        if star_count > 0:
            critical.append(ComplianceIssue(
                item=f"存在{star_count}处★号实质性参数，须逐条响应",
                status="需检查",
                severity="high",
                suggestion="技术方案和响应表必须逐条覆盖所有★号参数"
            ))

        # 检查报价
        if "超过采购预算" in text or "超过预算" in text:
            critical.append(ComplianceIssue(
                item="报价不得超过采购预算",
                status="需检查",
                severity="high",
                suggestion="报价必须严格控制在预算以内"
            ))

        # 检查保证金
        if "保证金" in text:
            critical.append(ComplianceIssue(
                item="投标保证金须按时交纳",
                status="需检查",
                severity="high",
                suggestion="确认保证金金额和到账时间"
            ))

        # 检查签章
        if "签字盖章" in text or "加盖公章" in text:
            critical.append(ComplianceIssue(
                item="投标文件须签字盖章",
                status="需检查",
                severity="high",
                suggestion="制作签章检查清单，逐页确认"
            ))

        # 检查业绩
        if "业绩" in text:
            warnings.append(ComplianceIssue(
                item="类似项目业绩要求",
                status="需准备",
                severity="medium",
                suggestion="整理业绩合同关键页、中标通知书和验收证明"
            ))

        # 检查国产化
        if "国产" in text or "信创" in text:
            warnings.append(ComplianceIssue(
                item="国产化适配要求",
                status="需确认",
                severity="medium",
                suggestion="确认产品国产化适配情况，准备适配证明"
            ))

        # 检查等保
        if "等保" in text:
            warnings.append(ComplianceIssue(
                item="等保合规要求",
                status="需确认",
                severity="medium",
                suggestion="确认等保测评方案和费用"
            ))

        # 人工确认项
        manual_items = [
            "企业资质认证有效性需人工确认",
            "项目人员资质和社保需人工确认",
            "业绩合同关键页完整性需人工确认",
            "报价合理性需人工确认",
            "技术方案具体实现细节需人工确认",
        ]

        # 建议
        suggestions = [
            "建议制作投标文件检查清单，逐项核对",
            "建议提前准备全部资格证明文件原件",
            "建议技术方案逐条对照评分项和★号参数",
            "建议报价前参考同类项目中标价",
            "建议投标前进行内部评审",
        ]

        compliance.critical_issues = critical
        compliance.warnings = warnings
        compliance.manual_review_items = manual_items
        compliance.suggestions = suggestions

        total_checks = len(critical) + len(warnings) + len(manual_items)
        passed = total_checks - len(critical)
        if total_checks > 0:
            compliance.pass_rate = f"{int(passed / total_checks * 100)}%"
        else:
            compliance.pass_rate = "需人工复核"

        if len(critical) > 0:
            compliance.overall_status = "存在高风险，建议补充材料后复核"
        else:
            compliance.overall_status = "未发现明显高风险，仍需人工确认"

        compliance.disclaimer = (
            "本报告由 BidPilot 自动生成，仅用于投标准备辅助。"
            "招标文件解释、投标文件最终内容、报价和合规判断"
            "均需由投标负责人、法务或专业人员人工复核确认。"
        )

        return AgentResult(
            agent=self.name,
            output=compliance.model_dump(),
            summary=f"合规审查：{compliance.overall_status}，致命问题{len(critical)}项，警告{len(warnings)}项",
            references=["compliance_checklist.md", "invalid_bid_risk_rules.md"]
        )

    def _build_prompt(self, context: AgentContext) -> str:
        return f"请基于招标文件进行合规审查：{context.tender_text[:2000]}"

    def _build_system_prompt(self) -> str:
        return "你是投标合规审查专家。所有合规结论标注'辅助审查，需人工复核'。不声称替代人工审查。"
