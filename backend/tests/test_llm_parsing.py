"""测试各 Agent 在非 MOCK 模式下的 LLM 输出解析逻辑 (llm_run)"""
import pytest
from backend.agents.base_agent import AgentContext
from backend.agents.tender_parser_agent import TenderParserAgent
from backend.agents.requirement_agent import RequirementAgent
from backend.agents.scoring_agent import ScoringAgent
from backend.agents.risk_agent import RiskAgent
from backend.agents.strategy_agent import StrategyAgent
from backend.agents.solution_agent import SolutionAgent
from backend.agents.business_agent import BusinessAgent
from backend.agents.response_table_agent import ResponseTableAgent
from backend.agents.compliance_agent import ComplianceAgent

@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_tender_parser_agent_llm_run():
    agent = TenderParserAgent()
    context = AgentContext(tender_text="测试文本")
    llm_output = """
    ```json
    {
        "项目名称": "智能网联测试平台",
        "采购人": "交通运输局",
        "预算": "500万元",
        "截止时间": "2026年8月1日",
        "项目类型": "智能交通"
    }
    ```
    """
    result = await agent.llm_run(context, llm_output)
    assert result.output["project_name"] == "智能网联测试平台"
    assert result.output["buyer"] == "交通运输局"
    assert result.output["budget"] == "500万元"
    assert result.output["deadline"] == "2026年8月1日"
    assert result.output["project_type"] == "智能交通"

@pytest.mark.anyio
async def test_requirement_agent_llm_run():
    agent = RequirementAgent()
    context = AgentContext(tender_text="测试文本")
    llm_output = """
    [
        {"requirement": "具有信息系统集成一级资质", "type": "资质要求", "mandatory": true, "risk_level": "high", "suggestion": "确认资质证书"},
        {"requirement": "项目经理具有高级信息系统项目管理师证书", "type": "人员要求", "mandatory": "是", "risk_level": "medium", "suggestion": "核对项目经理证书"}
    ]
    """
    result = await agent.llm_run(context, llm_output)
    assert len(result.output) == 2
    assert result.output[0]["requirement"] == "具有信息系统集成一级资质"
    assert result.output[0]["mandatory"] is True
    assert result.output[0]["risk_level"] == "high"
    assert result.output[1]["mandatory"] is True
    assert result.output[1]["risk_level"] == "medium"

@pytest.mark.anyio
async def test_scoring_agent_llm_run():
    agent = ScoringAgent()
    context = AgentContext(tender_text="测试文本")
    llm_output = """
    {
        "total_score": 100,
        "technical_score": 50,
        "business_score": 30,
        "price_score": 20,
        "items": [
            {"item": "设备协议支持", "score": 15, "weight": "高", "description": "支持Modbus等", "strategy": "重点编写协议接入"},
            {"item": "资质得分", "score": 5, "weight": "低", "description": "提供相关体系认证", "strategy": "按需提供证书"}
        ],
        "strategy_summary": "技术分占50分是关键"
    }
    """
    result = await agent.llm_run(context, llm_output)
    assert result.output["total_score"] == 100
    assert result.output["technical_score"] == 50
    assert len(result.output["items"]) == 2
    assert result.output["items"][0]["item"] == "设备协议支持"
    assert result.output["items"][0]["score"] == 15
    assert len(result.output["high_value_items"]) == 1

@pytest.mark.anyio
async def test_solution_agent_llm_run():
    agent = SolutionAgent()
    context = AgentContext(tender_text="测试文本")
    llm_output = """
# 顶层说明
这是大模型输出的方案前言。

## 1. 总体设计
这里是总体设计的详细内容，包含了系统物理架构。

## 2. 安全保障
这里是安全保障设计，我们需要确保数据加密。
    """
    result = await agent.llm_run(context, llm_output)
    assert len(result.output["sections"]) == 3
    assert result.output["sections"][0]["title"] == "项目背景与前言"
    assert result.output["sections"][1]["title"] == "1. 总体设计"
    assert "物理架构" in result.output["sections"][1]["content"]
    assert result.output["sections"][2]["title"] == "2. 安全保障"

@pytest.mark.anyio
async def test_llm_run_fallback_on_error():
    agent = TenderParserAgent()
    context = AgentContext(tender_text="项目名称：测试Fallback项目\n采购人：测试单位\n预算：300万元\n投标截止时间：2026-07-20")
    # 破坏 JSON 格式，触发 fallback
    llm_output = "这是一个坏掉的输出，根本不是JSON！"
    result = await agent.llm_run(context, llm_output)
    # 检查是否降级使用了 mock_run (正则提取)
    assert result.output["project_name"] == "测试Fallback项目"
    assert result.output["buyer"] == "测试单位"
    assert result.output["budget"] == "300万元"
