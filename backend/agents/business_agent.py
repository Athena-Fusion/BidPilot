"""BusinessAgent - 商务响应Agent"""
from backend.agents.base_agent import BaseAgent, AgentContext, AgentResult
from backend.models.schemas import BusinessResponse, BusinessItem


class BusinessAgent(BaseAgent):
    name = "BusinessAgent"
    description = "商务响应生成Agent"

    async def mock_run(self, context: AgentContext) -> AgentResult:
        text = context.tender_text
        items = []

        period = "需人工确认"
        if "90日" in text:
            period = "合同签订后90日内完成建设并上线试运行"
        elif "120日" in text:
            period = "合同签订后120日内完成建设并上线试运行"
        elif "60日" in text:
            period = "合同签订后60日内完成升级并上线试运行"
        items.append(BusinessItem(clause="服务周期", requirement=period, response="完全响应。我方承诺按期交付。"))

        items.append(BusinessItem(clause="付款方式", requirement="按招标文件规定", response="完全接受招标文件规定的付款方式和付款比例。"))

        warranty = "1年"
        if "2年" in text and "质保" in text:
            warranty = "2年"
        elif "3年" in text and "质保" in text:
            warranty = "3年"
        items.append(BusinessItem(clause="质保期", requirement=f"验收合格后{warranty}免费质保", response="完全响应。质保期内提供免费维护和技术支持。"))

        days = "5"
        if "不少于8天" in text:
            days = "8"
        elif "不少于10天" in text:
            days = "10"
        items.append(BusinessItem(clause="培训要求", requirement=f"不少于{days}天现场培训", response=f"完全响应。提供不少于{days}天的现场培训。"))

        resp_time = "2小时"
        if "不超过1小时" in text:
            resp_time = "1小时"
        items.append(BusinessItem(clause="售后服务", requirement=f"7x24技术支持，故障响应不超过{resp_time}", response=f"完全响应。故障响应不超过{resp_time}。"))

        items.append(BusinessItem(clause="知识产权", requirement="项目成果知识产权归采购人所有", response="完全响应。项目成果知识产权归采购人所有。"))
        items.append(BusinessItem(clause="保密条款", requirement="对项目相关信息严格保密", response="完全响应。所有项目人员签署保密协议。"))
        items.append(BusinessItem(clause="验收标准", requirement="按招标文件规定验收", response="完全响应。按招标文件验收标准组织验收。"))

        br = BusinessResponse(items=items, summary=f"共{len(items)}项商务条款，全部响应，无负偏离")
        return AgentResult(agent=self.name, output=br.model_dump(), summary=f"生成{len(items)}项商务响应", references=["business_response_template.md"])

    def _build_prompt(self, context: AgentContext) -> str:
        return f"请基于招标文件生成商务响应：{context.tender_text[:2000]}"

    def _build_system_prompt(self) -> str:
        return "你是投标商务响应专家。不确定内容标注'需人工确认'。"
