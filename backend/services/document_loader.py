"""DocumentLoader - 文档加载服务"""
import logging
from pathlib import Path
from backend.config import SAMPLE_TENDERS_DIR

logger = logging.getLogger(__name__)


class DocumentLoader:
    """文档加载器，支持 .txt/.md/.docx/.pdf"""

    SUPPORTED_EXTENSIONS = {".txt", ".md", ".docx", ".pdf"}

    @staticmethod
    async def load_from_sample(tender_id: str) -> str:
        """从示例文件目录加载招标文件

        匹配规则：sample_001 -> sample_tender_001_*.md
        """
        sample_dir = Path(SAMPLE_TENDERS_DIR)
        if not sample_dir.exists():
            raise FileNotFoundError(f"示例文件目录不存在: {sample_dir}")

        # 提取编号部分：sample_001 -> 001
        num_part = tender_id.split("_")[-1] if "_" in tender_id else tender_id

        # 按编号匹配文件：sample_tender_001_*.md
        for f in sorted(sample_dir.iterdir()):
            if f.suffix in (".md", ".txt") and f"_{num_part}_" in f.name:
                return f.read_text(encoding="utf-8")

        # 按ID子串匹配
        for f in sorted(sample_dir.iterdir()):
            if f.suffix in (".md", ".txt") and tender_id in f.name:
                return f.read_text(encoding="utf-8")

        raise FileNotFoundError(f"未找到示例招标文件: {tender_id}")

    @staticmethod
    async def load_from_upload(file_path: str) -> str:
        """从上传文件加载"""
        path = Path(file_path)
        ext = path.suffix.lower()

        if ext not in DocumentLoader.SUPPORTED_EXTENSIONS:
            raise ValueError(f"不支持的文件格式: {ext}，支持格式: {DocumentLoader.SUPPORTED_EXTENSIONS}")

        if ext in (".txt", ".md"):
            return path.read_text(encoding="utf-8")

        if ext == ".docx":
            return await DocumentLoader._load_docx(path)

        if ext == ".pdf":
            return await DocumentLoader._load_pdf(path)

        return ""

    @staticmethod
    async def _load_docx(path: Path) -> str:
        """加载 .docx 文件"""
        try:
            from docx import Document
            doc = Document(str(path))
            text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            if not text.strip():
                return "（docx文件内容为空或无法提取文本）"
            return text
        except ImportError:
            logger.warning("python-docx 未安装，无法解析 .docx 文件")
            return "（错误：python-docx 未安装，请执行 pip install python-docx）"
        except Exception as e:
            logger.error(f"解析 .docx 失败: {e}")
            return f"（解析 .docx 文件失败: {str(e)}）"

    @staticmethod
    async def _load_pdf(path: Path) -> str:
        """加载文本型 .pdf 文件"""
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(path))
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            if not text.strip():
                return "（PDF文件为扫描件或无法提取文本，建议使用OCR工具预处理）"
            return text
        except ImportError:
            logger.warning("pypdf 未安装，无法解析 .pdf 文件")
            return "（错误：pypdf 未安装，请执行 pip install pypdf）"
        except Exception as e:
            logger.error(f"解析 .pdf 失败: {e}")
            return f"（解析 .pdf 文件失败: {str(e)}）"

    @staticmethod
    def list_samples() -> list[dict]:
        """列出所有示例招标文件"""
        sample_dir = Path(SAMPLE_TENDERS_DIR)
        if not sample_dir.exists():
            return []
        results = []
        for f in sorted(sample_dir.iterdir()):
            if f.suffix in (".md", ".txt"):
                results.append({
                    "file_name": f.name,
                    "file_path": str(f),
                    "size": f.stat().st_size,
                })
        return results
