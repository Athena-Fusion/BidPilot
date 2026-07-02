"""TenderParserAgent - 招标文件解析Agent"""
import re
from backend.agents.base_agent import BaseAgent, AgentContext, AgentResult
from backend.models.schemas import BasicInfo


class TenderParserAgent(BaseAgent):
    name = "TenderParserAgent"
    description = "招标文件基本信息提取Agent"

    async def mock_run(self, context: AgentContext) -> AgentResult:
        text = context.tender_text
        info = BasicInfo()

        # 提取项目名称
        m = re.search(r'项目名称[：:]\s*(.+)', text)
        if m:
            info.project_name = m.group(1).strip()

        # 提取采购人
        m = re.search(r'采购人[：:]\s*(.+)', text)
        if m:
            info.buyer = m.group(1).strip()

        # 提取预算
        m = re.search(r'预算[：:]\s*人民币?(\d+万?元)', text)
        if m:
            info.budget = m.group(1)
        else:
            m = re.search(r'(\d+)万元', text)
            if m:
                info.budget = f"{m.group(1)}万元"

        # 提取截止时间
        m = re.search(r'投标截止时间[：:]\s*(.+)', text)
        if m:
            info.deadline = m.group(1).strip()

        # 提取建设周期
        m = re.search(r'建设周期[：:]\s*(.+)', text)
        if m:
            info.service_period = m.group(1).strip()

        # 提取交付地点
        m = re.search(r'交付地点[：:]\s*(.+)', text)
        if m:
            info.delivery_location = m.group(1).strip()

        # 提取保证金
        m = re.search(r'投标保证金[：:]\s*人民币?(\d+万?元)', text)
        if m:
            info.bid_bond = m.group(1)
        else:
            m = re.search(r'保证金[：:]\s*(.+)', text)
            if m:
                info.bid_bond = m.group(1).strip()

        # 提取采购范围
        m = re.search(r'采购范围[：:]\s*(.+)', text)
        if m:
            info.procurement_scope = m.group(1).strip()

        # 识别项目类型
        if "智慧园区" in text:
            info.project_type = "智慧园区"
        elif "数据中台" in text or "数据治理" in text:
            info.project_type = "数据中台"
        elif "政务服务" in text or "行政审批" in text:
            info.project_type = "政务服务"
        else:
            info.project_type = "信息化项目"

        # 未识别字段标注
        for field in ["project_name", "buyer", "budget", "deadline"]:
            if not getattr(info, field):
                setattr(info, field, "需人工确认")

        return AgentResult(
            agent=self.name,
            output=info.model_dump(),
            summary=f"提取项目基本信息：{info.project_name}，预算{info.budget}，类型{info.project_type}",
            references=["招标文件正文"]
        )

    async def llm_run(self, context: AgentContext, llm_output: str) -> AgentResult:
        try:
            from backend.utils.json_parser import extract_json
            data = extract_json(llm_output)
            
            # 规范化键值对，防止大模型返回不同的键名
            normalized_data = {}
            key_mapping = {
                "project_name": ["project_name", "项目名称", "name"],
                "buyer": ["buyer", "采购人", "采购单位", "业主"],
                "budget": ["budget", "预算", "最高限价", "采购预算"],
                "deadline": ["deadline", "截止时间", "投标截止时间"],
                "service_period": ["service_period", "建设周期", "服务期限", "工期"],
                "delivery_location": ["delivery_location", "交付地点", "实施地点"],
                "bid_bond": ["bid_bond", "投标保证金", "保证金"],
                "procurement_scope": ["procurement_scope", "采购范围", "采购内容"],
                "project_type": ["project_type", "项目类型"]
            }
            for target_key, aliases in key_mapping.items():
                val = ""
                for alias in aliases:
                    if alias in data:
                        val = data[alias]
                        break
                normalized_data[target_key] = str(val) if val is not None else ""
                
            info = BasicInfo(**normalized_data)
            
            # 未识别字段标注
            for field in ["project_name", "buyer", "budget", "deadline"]:
                if not getattr(info, field) or getattr(info, field) == "None":
                    setattr(info, field, "需人工确认")
                    
            # 若大模型未识别项目类型，自动进行推断
            if not info.project_type or info.project_type == "None":
                text = context.tender_text
                if "智慧园区" in text:
                    info.project_type = "智慧园区"
                elif "数据中台" in text or "数据治理" in text:
                    info.project_type = "数据中台"
                elif "政务服务" in text or "行政审批" in text:
                    info.project_type = "政务服务"
                else:
                    info.project_type = "信息化项目"

            return AgentResult(
                agent=self.name,
                output=info.model_dump(),
                summary=f"提取项目基本信息（LLM）：{info.project_name}，预算{info.budget}，类型{info.project_type}",
                references=["招标文件正文"]
            )
        except Exception as e:
            self.logger.warning(f"LLM 提取基本信息解析失败: {e}，将退回到规则模式提取")
            return await self.mock_run(context)

    def _build_prompt(self, context: AgentContext) -> str:
        return f"""请从以下招标文件中提取基本信息，包括项目名称、采购人、预算、截止时间、服务周期、交付地点、保证金、采购范围。

招标文件内容：
{context.tender_text[:3000]}

请以JSON格式返回。"""

    def _build_system_prompt(self) -> str:
        return "你是招标文件解析专家。请从招标文件中准确提取基本信息，不确定的内容标注'需人工确认'。"
