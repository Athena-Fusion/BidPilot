"""ExportService - 导出服务"""
import logging
import re
from datetime import datetime
from pathlib import Path
from backend.config import OUTPUT_DIR

logger = logging.getLogger(__name__)


class ExportService:
    """Markdown 报告导出服务"""

    _TASK_ID_PATTERN = re.compile(r"^analysis_[0-9a-f]{8}$")

    @staticmethod
    def _safe_report_name(name: str) -> str | None:
        """Accept only a plain Markdown filename, never a path supplied by data."""
        candidate = Path(name)
        if candidate.name != name or candidate.suffix.lower() != ".md":
            return None
        return name

    @staticmethod
    async def export_reports(task_id: str, reports: dict, report_type: str = "all") -> list[dict]:
        """导出报告到文件"""
        if not ExportService._TASK_ID_PATTERN.fullmatch(task_id):
            raise ValueError("无效的任务标识")
        output_dir = Path(OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 创建任务子目录
        task_dir = output_dir / task_id
        task_dir.mkdir(parents=True, exist_ok=True)

        exported = []
        files = reports.get("files", [])

        for f in files:
            name = ExportService._safe_report_name(f.get("name", "report.md"))
            if not name:
                logger.warning("跳过不安全的报告文件名")
                continue
            normalized_type = report_type.strip().lower()
            normalized_name = name.lower()
            if normalized_type not in {"", "all"} and normalized_type not in {normalized_name, normalized_name.removesuffix(".md")}:
                continue
            content = f.get("content", "")
            file_path = task_dir / name
            try:
                file_path.write_text(content, encoding="utf-8")
                exported.append({
                    "name": name,
                    "path": str(file_path),
                })
                logger.info(f"导出报告: {file_path}")
            except Exception as e:
                logger.error(f"导出报告失败 {name}: {e}")

        return exported

    @staticmethod
    async def export_single(task_id: str, filename: str, content: str) -> dict:
        """导出单个文件"""
        if not ExportService._TASK_ID_PATTERN.fullmatch(task_id):
            raise ValueError("无效的任务标识")
        safe_name = ExportService._safe_report_name(filename)
        if not safe_name:
            raise ValueError("报告文件名必须是 .md 文件名")
        output_dir = Path(OUTPUT_DIR) / task_id
        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = output_dir / safe_name
        file_path.write_text(content, encoding="utf-8")
        return {"name": filename, "path": str(file_path)}

    @staticmethod
    def list_outputs(task_id: str = "") -> list[dict]:
        """列出已导出的文件"""
        output_dir = Path(OUTPUT_DIR)
        if task_id:
            output_dir = output_dir / task_id
        if not output_dir.exists():
            return []
        results = []
        for f in sorted(output_dir.rglob("*.md")):
            results.append({
                "name": f.name,
                "path": str(f),
                "size": f.stat().st_size,
                "modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
            })
        return results
