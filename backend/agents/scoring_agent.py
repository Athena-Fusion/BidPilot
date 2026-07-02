"""ScoringAgent - 评分规则分析Agent"""
import re
from backend.agents.base_agent import BaseAgent, AgentContext, AgentResult
from backend.models.schemas import ScoringResult, ScoringItem


class ScoringAgent(BaseAgent):
    name = "ScoringAgent"
    description = "评分规则提取与分析Agent"

    async def mock_run(self, context: AgentContext) -> AgentResult:
        text = context.tender_text
        scoring = ScoringResult()

        # 提取总分和分项分数
        scoring.total_score = 100

        # 提取技术分、商务分、价格分
        m = re.search(r'技术部分[（(](\d+)分[）)]', text)
        if m:
            scoring.technical_score = float(m.group(1))
        m = re.search(r'商务部分[（(](\d+)分[）)]', text)
        if m:
            scoring.business_score = float(m.group(1))
        m = re.search(r'价格部分[（(](\d+)分[）)]', text)
        if m:
            scoring.price_score = float(m.group(1))

        # 提取评分项
        items = self._extract_scoring_items(text)
        scoring.items = items

        # 识别高权重项
        scoring.high_value_items = [
            item for item in items
            if item.score >= 10 or (scoring.total_score > 0 and item.score / scoring.total_score >= 0.1)
        ]

        # 生成策略摘要
        scoring.strategy_summary = self._build_strategy_summary(scoring)

        return AgentResult(
            agent=self.name,
            output=scoring.model_dump(),
            summary=f"技术{scoring.technical_score}分+商务{scoring.business_score}分+价格{scoring.price_score}分，高权重项{len(scoring.high_value_items)}个",
            references=["common_scoring_rules.md", "招标文件第三章"]
        )

    def _extract_scoring_items(self, text: str) -> list[ScoringItem]:
        """从表格中提取评分项"""
        items = []
        # 匹配表格行：| 评分项 | 分值 | ...
        pattern = r'\|\s*(.+?)\s*\|\s*(\d+)\s*\|\s*(.+?)(?=\s*\|)'
        matches = re.findall(pattern, text)

        for match in matches:
            name = match[0].strip()
            score = float(match[1])
            desc = match[2].strip() if len(match) > 2 else ""

            # 跳过表头
            if name in ["评分项", "项"] or "评分标准" in name:
                continue

            # 识别★号
            is_star = "★" in name
            strategy = ""
            if is_star:
                strategy = "★号实质性要求，必须重点响应，确保完全满足"
            elif score >= 10:
                strategy = "高权重项，需重点投入，确保高分"

            items.append(ScoringItem(
                item=name.replace("★", "").strip(),
                score=score,
                weight="高" if score >= 10 else ("中" if score >= 5 else "低"),
                description=desc[:200],
                strategy=strategy
            ))

        # 如果没有从表格提取到，使用默认
        if not items:
            items = self._default_items(text)

        return items

    def _default_items(self, text: str) -> list[ScoringItem]:
        if "智慧园区" in text:
            return [
                ScoringItem(item="技术方案总体架构设计", score=10, weight="高", strategy="高权重项，需重点投入"),
                ScoringItem(item="设备接入管理方案", score=10, weight="高", strategy="★号实质性要求，必须重点响应"),
                ScoringItem(item="国产化适配方案", score=10, weight="高", strategy="★号实质性要求，必须重点响应"),
                ScoringItem(item="数据安全方案", score=8, weight="中", strategy="★号实质性要求，必须重点响应"),
                ScoringItem(item="数据可视化方案", score=8, weight="中", strategy="需体现大屏设计和实时性"),
                ScoringItem(item="统一门户系统方案", score=8, weight="中", strategy="需体现SSO和多终端适配"),
            ]
        elif "数据中台" in text:
            return [
                ScoringItem(item="数据治理方案", score=15, weight="高", strategy="★号实质性要求，最高权重项"),
                ScoringItem(item="数据交换共享方案", score=12, weight="高", strategy="★号实质性要求，需重点响应"),
                ScoringItem(item="数据中台总体架构", score=12, weight="高", strategy="高权重项，需重点投入"),
                ScoringItem(item="数据质量管控方案", score=10, weight="高", strategy="★号实质性要求，必须重点响应"),
            ]
        else:
            return [
                ScoringItem(item="移动端适配方案", score=12, weight="高", strategy="★号实质性要求，必须重点响应"),
                ScoringItem(item="办件流程优化方案", score=12, weight="高", strategy="★号实质性要求，必须重点响应"),
                ScoringItem(item="平台升级技术方案", score=10, weight="高", strategy="高权重项，需重点投入"),
            ]

    def _build_strategy_summary(self, scoring: ScoringResult) -> str:
        parts = []
        if scoring.technical_score > 0:
            parts.append(f"技术分{scoring.technical_score}分占比最高，是得分关键")
        if scoring.high_value_items:
            star_items = [i for i in scoring.high_value_items if "★" in i.item or "实质性" in i.strategy]
            if star_items:
                parts.append(f"其中{len(star_items)}项为★号实质性要求，必须完全响应")
        parts.append("建议技术方案重点覆盖高权重评分项")
        return "；".join(parts)

    async def llm_run(self, context: AgentContext, llm_output: str) -> AgentResult:
        try:
            from backend.utils.json_parser import extract_json
            data = extract_json(llm_output)
            
            scoring = ScoringResult()
            scoring.total_score = float(data.get("total_score", data.get("总分", 100)))
            scoring.technical_score = float(data.get("technical_score", data.get("技术分", 0)))
            scoring.business_score = float(data.get("business_score", data.get("商务分", 0)))
            scoring.price_score = float(data.get("price_score", data.get("价格分", 0)))
            
            items_data = data.get("items", data.get("评分项", []))
            items = []
            for item in items_data:
                if not isinstance(item, dict):
                    continue
                name = item.get("item", item.get("name", item.get("评分项", "")))
                if not name:
                    continue
                score = float(item.get("score", item.get("分值", 0)))
                weight = item.get("weight", item.get("权重", "中"))
                desc = item.get("description", item.get("评分标准", ""))
                strategy = item.get("strategy", item.get("策略", ""))
                
                items.append(ScoringItem(
                    item=name.replace("★", "").strip(),
                    score=score,
                    weight=weight,
                    description=desc[:200],
                    strategy=strategy
                ))
            
            scoring.items = items
            # 识别高权重评分项
            scoring.high_value_items = [
                item for item in items
                if item.score >= 10 or (scoring.total_score > 0 and item.score / scoring.total_score >= 0.1)
            ]
            scoring.strategy_summary = data.get("strategy_summary", data.get("策略摘要", ""))
            if not scoring.strategy_summary:
                scoring.strategy_summary = self._build_strategy_summary(scoring)
                
            return AgentResult(
                agent=self.name,
                output=scoring.model_dump(),
                summary=f"技术{scoring.technical_score}分+商务{scoring.business_score}分+价格{scoring.price_score}分（LLM），高权重项{len(scoring.high_value_items)}个",
                references=["招标文件第三章"]
            )
        except Exception as e:
            self.logger.warning(f"LLM 提取评分规则解析失败: {e}，将退回到规则模式提取")
            return await self.mock_run(context)

    def _build_prompt(self, context: AgentContext) -> str:
        return f"""请从以下招标文件中提取评分规则，包括技术分、商务分、价格分及各评分项的分值和评分标准。

请以 JSON 格式返回，包含字段：total_score, technical_score, business_score, price_score, items (包含 item, score, weight, description, strategy) 和 strategy_summary。

招标文件内容：
{context.tender_text[:3000]}"""

    def _build_system_prompt(self) -> str:
        return "你是投标评分分析专家。请准确提取评分规则，识别高权重项和★号实质性要求。"
