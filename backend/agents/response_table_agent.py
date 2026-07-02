"""ResponseTableAgent - 响应表/偏离表生成Agent"""
import re
from backend.agents.base_agent import BaseAgent, AgentContext, AgentResult
from backend.models.schemas import ResponseTables, ResponseTableRow


class ResponseTableAgent(BaseAgent):
    name = "ResponseTableAgent"
    description = "响应表和偏离表生成Agent"

    async def mock_run(self, context: AgentContext) -> AgentResult:
        text = context.tender_text
        tables = ResponseTables()

        # 提取★号技术参数
        tech_rows = self._extract_star_params(text)
        if not tech_rows:
            tech_rows = self._default_tech_rows(text)
        tables.technical_response = tech_rows

        # 商务响应表
        tables.business_response = self._build_business_rows(text)

        # 技术偏离表
        tables.technical_deviation = self._build_tech_deviation(tech_rows)

        # 商务偏离表
        tables.business_deviation = self._build_biz_deviation(text)

        total = (len(tables.technical_response) + len(tables.business_response) +
                 len(tables.technical_deviation) + len(tables.business_deviation))

        return AgentResult(
            agent=self.name,
            output=tables.model_dump(),
            summary=f"生成{total}条响应表记录，技术响应{len(tables.technical_response)}条，商务响应{len(tables.business_response)}条",
            references=["business_response_template.md"]
        )

    def _extract_star_params(self, text: str) -> list[ResponseTableRow]:
        rows = []
        idx = 1
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if "★" in line and len(line) > 5:
                req = line.replace("★", "").strip()
                if len(req) < 5:
                    continue
                rows.append(ResponseTableRow(
                    id=idx,
                    tender_requirement=req[:150],
                    response="完全响应。" + self._generate_response(req),
                    deviation="无偏离",
                    proof="详见技术方案对应章节",
                    risk_level="low"
                ))
                idx += 1
        return rows

    def _generate_response(self, req: str) -> str:
        if "并发" in req:
            return "本方案采用分布式架构，支持不少于1000个并发用户访问。"
        elif "设备协议" in req or "协议接入" in req:
            return "本方案支持250+种设备协议接入，超过要求。"
        elif "国产" in req or "适配" in req:
            return "本方案全面适配国产CPU、操作系统、数据库和中间件。"
        elif "加密" in req or "安全" in req:
            return "本方案支持SM2/SM3/SM4国密算法和AES256加密。"
        elif "日志" in req or "审计" in req:
            return "本方案记录全操作日志，保留不少于365天，日志不可篡改。"
        elif "元数据" in req:
            return "本方案支持技术元数据和业务元数据全量管理。"
        elif "数据源" in req:
            return "本方案支持15+种数据源接入。"
        elif "REST" in req or "API" in req:
            return "本方案提供标准RESTful API，支持OAuth2.0认证。"
        elif "质量" in req:
            return "本方案支持完整性、准确性、一致性、及时性、唯一性五维度检测。"
        elif "等保" in req:
            return "本方案满足等保三级要求。"
        elif "移动" in req or "适配" in req:
            return "本方案全面适配iOS、Android和微信小程序。"
        elif "流程" in req or "优化" in req:
            return "本方案承诺优化20+高频办件流程，时限压缩30%以上。"
        else:
            return "本方案完全满足该项要求。需人工确认具体实现细节。"

    def _default_tech_rows(self, text: str) -> list[ResponseTableRow]:
        if "智慧园区" in text:
            return [
                ResponseTableRow(id=1, tender_requirement="支持不少于500个并发用户访问", response="完全响应。分布式架构支持1000+并发。", deviation="正偏离", proof="详见技术方案3.1", risk_level="low"),
                ResponseTableRow(id=2, tender_requirement="支持不少于200种设备协议接入", response="完全响应。支持250+种协议。", deviation="正偏离", proof="详见技术方案4.2", risk_level="low"),
                ResponseTableRow(id=3, tender_requirement="全面适配国产CPU/OS/DB/中间件", response="完全响应。已适配飞腾/鲲鹏+麒麟/UOS+达梦/金仓+东方通。", deviation="无偏离", proof="详见技术方案7", risk_level="low"),
            ]
        elif "数据中台" in text:
            return [
                ResponseTableRow(id=1, tender_requirement="支持元数据管理", response="完全响应。支持技术元数据和业务元数据全量管理。", deviation="无偏离", proof="详见技术方案4.1", risk_level="low"),
                ResponseTableRow(id=2, tender_requirement="支持不少于10种数据源接入", response="完全响应。支持15+种数据源。", deviation="正偏离", proof="详见技术方案4.3", risk_level="low"),
            ]
        else:
            return [
                ResponseTableRow(id=1, tender_requirement="适配iOS和Android主流机型", response="完全响应。采用uni-app跨端方案。", deviation="无偏离", proof="详见技术方案4.2", risk_level="low"),
                ResponseTableRow(id=2, tender_requirement="提供微信小程序版本", response="完全响应。同一套代码编译小程序。", deviation="无偏离", proof="详见技术方案4.2", risk_level="low"),
            ]

    def _build_business_rows(self, text: str) -> list[ResponseTableRow]:
        rows = [
            ResponseTableRow(id=1, tender_requirement="服务周期", response="完全响应", deviation="无偏离", proof="详见商务响应", risk_level="low"),
            ResponseTableRow(id=2, tender_requirement="付款方式", response="完全接受", deviation="无偏离", proof="详见商务响应", risk_level="low"),
            ResponseTableRow(id=3, tender_requirement="质保期", response="完全响应", deviation="无偏离", proof="详见商务响应", risk_level="low"),
            ResponseTableRow(id=4, tender_requirement="知识产权", response="完全响应，归采购人所有", deviation="无偏离", proof="详见商务响应", risk_level="low"),
        ]
        return rows

    def _build_tech_deviation(self, tech_rows: list[ResponseTableRow]) -> list[ResponseTableRow]:
        deviation = []
        for row in tech_rows:
            if row.deviation and row.deviation != "无偏离":
                deviation.append(ResponseTableRow(
                    id=row.id,
                    tender_requirement=row.tender_requirement,
                    response=row.response,
                    deviation=row.deviation,
                    proof=row.proof,
                    risk_level="low"
                ))
        return deviation

    def _build_biz_deviation(self, text: str) -> list[ResponseTableRow]:
        return []

    async def llm_run(self, context: AgentContext, llm_output: str) -> AgentResult:
        try:
            from backend.utils.json_parser import extract_json
            data = extract_json(llm_output)
            
            tables = ResponseTables()
            
            def parse_rows(raw_list):
                rows = []
                if not isinstance(raw_list, list):
                    return rows
                for idx, item in enumerate(raw_list, 1):
                    if not isinstance(item, dict):
                        continue
                    req = item.get("tender_requirement", item.get("招标要求", ""))
                    if not req:
                        continue
                    resp = item.get("response", item.get("响应内容", ""))
                    dev = item.get("deviation", item.get("偏差", "无偏离"))
                    proof = item.get("proof", item.get("证明材料", "详见技术方案"))
                    risk = item.get("risk_level", item.get("风险等级", "low")).lower()
                    if risk not in {"high", "medium", "low"}:
                        risk = "low"
                        
                    rows.append(ResponseTableRow(
                        id=item.get("id", idx),
                        tender_requirement=req,
                        response=resp,
                        deviation=dev,
                        proof=proof,
                        risk_level=risk
                    ))
                return rows
                
            tables.technical_response = parse_rows(data.get("technical_response", []))
            tables.business_response = parse_rows(data.get("business_response", []))
            tables.technical_deviation = parse_rows(data.get("technical_deviation", []))
            tables.business_deviation = parse_rows(data.get("business_deviation", []))
            
            total = (len(tables.technical_response) + len(tables.business_response) +
                     len(tables.technical_deviation) + len(tables.business_deviation))
                     
            if total == 0:
                raise ValueError("未生成任何响应表行")
                
            return AgentResult(
                agent=self.name,
                output=tables.model_dump(),
                summary=f"生成{total}条响应表记录（LLM），技术响应{len(tables.technical_response)}条，商务响应{len(tables.business_response)}条",
                references=["LLM响应表分析"]
            )
        except Exception as e:
            self.logger.warning(f"LLM 响应表生成解析失败: {e}，将退回到规则模式提取")
            return await self.mock_run(context)

    def _build_prompt(self, context: AgentContext) -> str:
        return f"""请基于以下招标文件生成技术与商务响应表及偏离表：
{context.tender_text[:2000]}

请以 JSON 格式返回，包含以下字段：
- technical_response (包含 id, tender_requirement, response, deviation, proof, risk_level 的数组)
- business_response (同上，商务响应)
- technical_deviation (偏离的技术响应项数组)
- business_deviation (偏离的商务响应项数组)"""

    def _build_system_prompt(self) -> str:
        return "你是投标响应表专家。强制条款默认完全响应，不主动生成负偏离，不确定内容标注'需人工确认'。"
