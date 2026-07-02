"""BidPilot JSON 解析辅助工具"""
import re
import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

def extract_json(text: str) -> Any:
    """从文本中提取 JSON 块并解析"""
    if not text:
        raise ValueError("输入文本为空")
        
    text_stripped = text.strip()
    
    # 尝试直接解析整段文本
    try:
        return json.loads(text_stripped)
    except json.JSONDecodeError:
        pass

    # 尝试匹配 ```json ... ``` 块
    m = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL | re.IGNORECASE)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except json.JSONDecodeError as e:
            logger.debug(f"解析 markdown json 块失败: {e}")
            
    # 尝试匹配包含在大括号或中括号中的最外层 JSON
    m = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except json.JSONDecodeError as e:
            logger.debug(f"解析大括号/中括号 JSON 失败: {e}")
            
    raise ValueError("未能从 LLM 输出中提取出有效的 JSON 结构")
