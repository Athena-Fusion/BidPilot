"""ReportAgent - 投标分析报告生成Agent"""
from datetime import datetime
from backend.agents.base_agent import BaseAgent, AgentContext, AgentResult
from backend.models.schemas import Reports, ReportFile


class ReportAgent(BaseAgent):
    name = "ReportAgent"
    description = "投标分析报告生成Agent"

    async def mock_run(self, context: AgentContext) -> AgentResult:
        prev = context.previous_outputs or {}
        basic_info = prev.get("basic_info", {})
        tender_name = basic_info.get("project_name", "未命名项目")
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        files = []

        # 综合分析报告
        files.append(ReportFile(name="tender_analysis_report.md", content=self._analysis_report(tender_name, prev, now)))
        # 风险检查清单
        files.append(ReportFile(name="risk_checklist.md", content=self._risk_report(tender_name, prev, now)))
        # 投标策略报告
        files.append(ReportFile(name="bid_strategy_report.md", content=self._strategy_report(tender_name, prev, now)))
        # 技术方案初稿
        files.append(ReportFile(name="technical_solution_draft.md", content=self._solution_report(tender_name, prev, now)))
        # 商务响应表
        files.append(ReportFile(name="business_response_table.md", content=self._business_response_report(tender_name, prev, now)))
        # 技术响应表
        files.append(ReportFile(name="technical_response_table.md", content=self._technical_response_report(tender_name, prev, now)))
        # 偏离表
        files.append(ReportFile(name="deviation_table.md", content=self._deviation_report(tender_name, prev, now)))
        # 合规审查报告
        files.append(ReportFile(name="compliance_review_report.md", content=self._compliance_report(tender_name, prev, now)))

        reports = Reports(files=files)
        return AgentResult(
            agent=self.name,
            output=reports.model_dump(),
            summary=f"生成{len(files)}份报告",
            references=[]
        )

    def _disclaimer(self) -> str:
        return "\n---\n**免责声明**：本报告由 BidPilot 自动生成，仅用于投标准备辅助。招标文件解释、投标文件最终内容、报价和合规判断均需由投标负责人、法务或专业人员人工复核确认。\n"

    def _analysis_report(self, name: str, prev: dict, now: str) -> str:
        from backend.config import MOCK_MODE
        bi = prev.get("basic_info", {})
        reqs = prev.get("requirements", [])
        scoring = prev.get("scoring", {})
        mode_label = "Mock 演示模式" if MOCK_MODE else "AI 智能模式 (LLM)"
        lines = [
            f"# 招标分析报告 - {name}", f"\n生成时间：{now}  \n生成模式：{mode_label}\n",
            "## 基本信息",
            f"- 项目名称：{bi.get('project_name', '需人工确认')}",
            f"- 采购人：{bi.get('buyer', '需人工确认')}",
            f"- 预算：{bi.get('budget', '需人工确认')}",
            f"- 截止时间：{bi.get('deadline', '需人工确认')}",
            f"- 服务周期：{bi.get('service_period', '需人工确认')}",
            f"- 保证金：{bi.get('bid_bond', '需人工确认')}",
            "\n## 资格要求",
        ]
        for r in reqs[:10]:
            rl = r.get("risk_level", "low")
            tag = {"high": "🔴高风险", "medium": "🟡中风险", "low": "🟢低风险"}.get(rl, "🟢低风险")
            lines.append(f"- {tag} [{r.get('type', '')}] {r.get('requirement', '')}")
        lines.append("\n## 评分规则")
        lines.append(f"- 技术分：{scoring.get('technical_score', 0)}")
        lines.append(f"- 商务分：{scoring.get('business_score', 0)}")
        lines.append(f"- 价格分：{scoring.get('price_score', 0)}")
        for item in scoring.get("high_value_items", [])[:5]:
            lines.append(f"- ⭐ {item.get('item', '')}（{item.get('score', 0)}分）")
        lines.append(self._disclaimer())
        return "\n".join(lines)

    def _risk_report(self, name: str, prev: dict, now: str) -> str:
        risks = prev.get("risks", [])
        lines = [f"# 风险检查清单 - {name}", f"\n生成时间：{now}\n"]
        high = [r for r in risks if r.get("severity") == "high"]
        medium = [r for r in risks if r.get("severity") == "medium"]
        low = [r for r in risks if r.get("severity") == "low"]
        lines.append(f"## 高风险（{len(high)}项）")
        for r in high:
            lines.append(f"- **{r.get('risk_type', '')}**：{r.get('risk', '')}")
            lines.append(f"  - 证据：{r.get('evidence', '')}")
            lines.append(f"  - 处理：{r.get('action', '')}")
        lines.append(f"\n## 中风险（{len(medium)}项）")
        for r in medium:
            lines.append(f"- **{r.get('risk_type', '')}**：{r.get('risk', '')}")
        lines.append(f"\n## 低风险（{len(low)}项）")
        for r in low:
            lines.append(f"- {r.get('risk', '')}")
        lines.append(self._disclaimer())
        return "\n".join(lines)

    def _strategy_report(self, name: str, prev: dict, now: str) -> str:
        st = prev.get("strategy", {})
        lines = [
            f"# 投标策略报告 - {name}", f"\n生成时间：{now}\n",
            f"## 投标建议：{st.get('recommendation', '需人工确认')}",
            f"## 胜算评估\n{st.get('win_assessment', '')}",
            "\n## 核心得分策略",
        ]
        for s in st.get("score_strategy", []):
            lines.append(f"- {s}")
        lines.append(f"\n## 报价建议\n{st.get('price_suggestion', '')}")
        lines.append("\n## 材料准备清单")
        for m in st.get("material_checklist", []):
            lines.append(f"- [ ] {m}")
        lines.append(self._disclaimer())
        return "\n".join(lines)

    def _solution_report(self, name: str, prev: dict, now: str) -> str:
        sol = prev.get("solution", {})
        lines = [f"# 技术方案初稿 - {name}", f"\n生成时间：{now}\n"]
        for s in sol.get("sections", []):
            lines.append(f"## {s.get('title', '')}")
            lines.append(s.get("content", ""))
            if s.get("needs_review"):
                lines.append("*（需人工确认）*")
            lines.append("")
        lines.append(self._disclaimer())
        return "\n".join(lines)

    def _cell(self, value) -> str:
        text = "" if value is None else str(value)
        return text.replace("|", "\\|").replace("\r", " ").replace("\n", "<br>").strip()

    def _business_response_report(self, name: str, prev: dict, now: str) -> str:
        business = prev.get("business_response", {})
        lines = [f"# 商务响应表 - {name}", f"\n生成时间：{now}\n", "| 序号 | 条款 | 招标要求 | 响应内容 | 人工确认 |", "| --- | --- | --- | --- | --- |"]
        for idx, item in enumerate(business.get("items", []), 1):
            review = "是" if item.get("needs_review") else "否"
            lines.append(f"| {idx} | {self._cell(item.get('clause', ''))} | {self._cell(item.get('requirement', ''))} | {self._cell(item.get('response', ''))} | {review} |")
        if business.get("summary"):
            lines.append(f"\n## 汇总\n{business.get('summary')}")
        lines.append(self._disclaimer())
        return "\n".join(lines)

    def _technical_response_report(self, name: str, prev: dict, now: str) -> str:
        tables = prev.get("response_tables", {})
        rows = tables.get("technical_response", [])
        lines = [f"# 技术响应表 - {name}", f"\n生成时间：{now}\n", "| 序号 | 招标要求 | 响应内容 | 响应类型 | 证明材料 | 风险等级 |", "| --- | --- | --- | --- | --- | --- |"]
        for row in rows:
            lines.append(f"| {row.get('id', '')} | {self._cell(row.get('tender_requirement', ''))} | {self._cell(row.get('response', ''))} | {self._cell(row.get('deviation', ''))} | {self._cell(row.get('proof', ''))} | {row.get('risk_level', '')} |")
        lines.append(self._disclaimer())
        return "\n".join(lines)

    def _deviation_report(self, name: str, prev: dict, now: str) -> str:
        tables = prev.get("response_tables", {})
        technical = tables.get("technical_deviation", [])
        business = tables.get("business_deviation", [])
        lines = [f"# 偏离表 - {name}", f"\n生成时间：{now}\n", "## 技术偏离表", "| 序号 | 招标要求 | 响应内容 | 偏离类型 | 证明材料 |", "| --- | --- | --- | --- | --- |"]
        if technical:
            for row in technical:
                lines.append(f"| {row.get('id', '')} | {self._cell(row.get('tender_requirement', ''))} | {self._cell(row.get('response', ''))} | {self._cell(row.get('deviation', ''))} | {self._cell(row.get('proof', ''))} |")
        else:
            lines.append("| - | 未识别到技术偏离项 | 默认完全响应，需人工复核 | 无偏离 | - |")
        lines.extend(["\n## 商务偏离表", "| 序号 | 招标要求 | 响应内容 | 偏离类型 | 证明材料 |", "| --- | --- | --- | --- | --- |"])
        if business:
            for row in business:
                lines.append(f"| {row.get('id', '')} | {self._cell(row.get('tender_requirement', ''))} | {self._cell(row.get('response', ''))} | {self._cell(row.get('deviation', ''))} | {self._cell(row.get('proof', ''))} |")
        else:
            lines.append("| - | 未识别到商务偏离项 | 默认完全响应，需人工复核 | 无偏离 | - |")
        lines.append("\n说明：系统不会自动生成负偏离；无法确定内容应标注为需人工确认。")
        lines.append(self._disclaimer())
        return "\n".join(lines)

    def _compliance_report(self, name: str, prev: dict, now: str) -> str:
        comp = prev.get("compliance", {})
        lines = [
            f"# 合规审查报告 - {name}", f"\n生成时间：{now}\n",
            f"## 总体状态：{comp.get('overall_status', '需人工复核')}",
            f"## 通过率：{comp.get('pass_rate', '需人工复核')}",
            "\n## 致命问题",
        ]
        for c in comp.get("critical_issues", []):
            lines.append(f"- 🔴 {c.get('item', '')}：{c.get('suggestion', '')}")
        lines.append("\n## 警告")
        for w in comp.get("warnings", []):
            lines.append(f"- 🟡 {w.get('item', '')}：{w.get('suggestion', '')}")
        lines.append("\n## 待人工确认项")
        for m in comp.get("manual_review_items", []):
            lines.append(f"- {m}")
        lines.append("\n## 建议")
        for s in comp.get("suggestions", []):
            lines.append(f"- {s}")
        lines.append(self._disclaimer())
        return "\n".join(lines)

    def _build_prompt(self, context: AgentContext) -> str:
        return "请基于分析结果生成投标分析报告。"

    def _build_system_prompt(self) -> str:
        return "你是投标报告撰写专家。所有报告须包含免责声明。"
