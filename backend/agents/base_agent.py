"""BidPilot BaseAgent - 所有 Agent 的基类"""
import time
import logging
from typing import Any, Optional
from backend.config import MOCK_MODE

logger = logging.getLogger(__name__)


class LLMClient:
    """统一 LLM 调用抽象层"""

    def __init__(self):
        from backend.config import (
            MOCK_MODE, OPENAI_COMPATIBLE_MODE, CUSTOM_MODEL_MODE,
            LLM_API_KEY, LLM_BASE_URL, LLM_MODEL
        )
        self.mock_mode = MOCK_MODE
        self.openai_mode = OPENAI_COMPATIBLE_MODE
        self.custom_mode = CUSTOM_MODEL_MODE
        self.api_key = LLM_API_KEY
        self.base_url = LLM_BASE_URL
        self.model = LLM_MODEL

    async def chat(self, prompt: str, system: str = "") -> str:
        """调用 LLM，mock 模式返回空字符串由 Agent 自行处理"""
        if self.mock_mode:
            return ""
        if self.openai_mode and self.api_key and self.base_url:
            return await self._openai_chat(prompt, system)
        if self.custom_mode and self.api_key and self.base_url:
            return await self._custom_chat(prompt, system)
        logger.warning("未配置可用模型，返回空结果")
        return ""

    async def _openai_chat(self, prompt: str, system: str = "") -> str:
        """OpenAI Compatible 接口调用"""
        try:
            import httpx
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 4096
            }
            async with httpx.AsyncClient(timeout=60) as client:
                resp = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers
                )
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"OpenAI Compatible 调用失败: {e}")
            return ""

    async def _custom_chat(self, prompt: str, system: str = "") -> str:
        """自定义模型接口调用（预留）"""
        logger.info("自定义模型接口尚未实现，返回空结果")
        return ""


# 全局 LLM 客户端
llm_client = LLMClient()


class AgentContext:
    """Agent 执行上下文"""

    def __init__(
        self,
        tender_id: str = "",
        tender_text: str = "",
        basic_info: Optional[dict] = None,
        requirements: Optional[list] = None,
        scoring: Optional[dict] = None,
        risks: Optional[list] = None,
        knowledge_refs: Optional[list] = None,
        previous_outputs: Optional[dict] = None,
    ):
        self.tender_id = tender_id
        self.tender_text = tender_text
        self.basic_info = basic_info or {}
        self.requirements = requirements or []
        self.scoring = scoring or {}
        self.risks = risks or []
        self.knowledge_refs = knowledge_refs or []
        self.previous_outputs = previous_outputs or {}


class AgentResult:
    """Agent 执行结果"""

    def __init__(
        self,
        agent: str,
        output: Any = None,
        summary: str = "",
        references: Optional[list] = None,
        warnings: Optional[list] = None,
    ):
        self.agent = agent
        self.output = output
        self.summary = summary
        self.references = references or []
        self.warnings = warnings or []


class BaseAgent:
    """所有 Agent 的基类"""

    name: str = "BaseAgent"
    description: str = ""

    def __init__(self):
        self.logger = logging.getLogger(self.name)

    async def run(self, context: AgentContext) -> AgentResult:
        """执行 Agent，自动选择 mock 或 LLM 模式"""
        start = time.time()
        try:
            if MOCK_MODE:
                result = await self.mock_run(context)
            else:
                llm_output = await llm_client.chat(
                    prompt=self._build_prompt(context),
                    system=self._build_system_prompt()
                )
                if llm_output:
                    result = await self.llm_run(context, llm_output)
                else:
                    result = await self.mock_run(context)

            duration = int((time.time() - start) * 1000)
            result.agent = self.name
            self.logger.info(f"{self.name} 完成, 耗时 {duration}ms, 摘要: {result.summary}")
            return result
        except Exception as e:
            self.logger.error(f"{self.name} 执行失败: {e}")
            return AgentResult(
                agent=self.name,
                output=None,
                summary=f"执行失败: {str(e)}",
                warnings=[str(e)]
            )

    async def mock_run(self, context: AgentContext) -> AgentResult:
        """Mock 模式执行，子类必须实现"""
        raise NotImplementedError

    async def llm_run(self, context: AgentContext, llm_output: str) -> AgentResult:
        """LLM 模式执行，子类可选实现"""
        return await self.mock_run(context)

    def _build_prompt(self, context: AgentContext) -> str:
        """构建 LLM prompt，子类可选覆盖"""
        return f"分析以下招标文件内容：\n\n{context.tender_text[:3000]}"

    def _build_system_prompt(self) -> str:
        """构建 LLM system prompt，子类可选覆盖"""
        return f"你是{self.description}。请严格按照招标文件内容进行分析，不确定的内容标注'需人工确认'。"
