"""BidPilot 后端配置模块"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 目录定位
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent


def _resolve_path(value: str | None, default: Path) -> Path:
    """Resolve configured paths consistently from the project root."""
    if not value:
        return default
    path = Path(value)
    return path if path.is_absolute() else PROJECT_ROOT / path


def _positive_int(name: str, default: int) -> int:
    """Read a positive integer setting without making startup fragile."""
    try:
        value = int(os.getenv(name, str(default)))
    except ValueError:
        return default
    return value if value > 0 else default


def _csv_setting(name: str, default: str = "") -> list[str]:
    """Parse comma-separated settings while dropping empty entries."""
    return [item.strip() for item in os.getenv(name, default).split(",") if item.strip()]

# 运行模式
MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"
OPENAI_COMPATIBLE_MODE = os.getenv("OPENAI_COMPATIBLE_MODE", "false").lower() == "true"
CUSTOM_MODEL_MODE = os.getenv("CUSTOM_MODEL_MODE", "false").lower() == "true"

# LLM 配置
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-v4-flash")

# 服务配置
BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
CORS_ORIGINS = _csv_setting("CORS_ORIGINS", "*")
MAX_UPLOAD_SIZE_BYTES = _positive_int("MAX_UPLOAD_SIZE_BYTES", 10 * 1024 * 1024)
ANALYSIS_CACHE_MAX_ENTRIES = _positive_int("ANALYSIS_CACHE_MAX_ENTRIES", 100)

# 数据目录
DATA_DIR = _resolve_path(os.getenv("DATA_DIR"), BASE_DIR / "data")
SAMPLE_TENDERS_DIR = DATA_DIR / "sample_tenders"
KNOWLEDGE_BASE_DIR = DATA_DIR / "knowledge_base"
OUTPUT_DIR = _resolve_path(os.getenv("OUTPUT_DIR"), DATA_DIR / "outputs")

# 确保目录存在
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 版本
VERSION = "0.1.0"


def get_mode_label() -> str:
    """获取当前模式标签"""
    if MOCK_MODE:
        return "Mock 演示模式"
    elif OPENAI_COMPATIBLE_MODE:
        return "OpenAI Compatible 模式"
    elif CUSTOM_MODEL_MODE:
        return "自定义模型模式"
    else:
        return "未配置模型"
