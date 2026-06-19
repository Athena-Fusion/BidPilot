"""ExportService - 导出服务"""
import logging
from datetime import datetime
from pathlib import Path
from backend.config import OUTPUT_DIR

logger = logging.getLogger(__name__)


class ExportService:
    """Markdown 报告导出服务"""

    @staticmethod
    async def export_reports(task_id: str, reports: dict, report_type: str = "all") -> list[dict]:
        """导出报告到文件"""
        output_dir = Path(OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 创建任务子目录
        task_dir = output_dir / task_id
        task_dir.mkdir(parents=True, exist_ok=True)

        exported = []
        files = reports.get("files", [])

        for f in files:
            name = f.get("name", "report.md")
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
        output_dir = Path(OUTPUT_DIR) / task_id
        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = output_dir / filename
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
