"""KnowledgeService - 知识库检索服务"""
import logging
from pathlib import Path
from backend.config import KNOWLEDGE_BASE_DIR
from backend.models.schemas import KnowledgeRef

logger = logging.getLogger(__name__)


class KnowledgeService:
    """本地 Markdown 知识库关键词检索"""

    # 项目类型关键词映射
    TYPE_KEYWORDS = {
        "智慧园区": ["园区", "设备接入", "IBMS", "BIM", "数字孪生", "物联网", "可视化大屏", "统一门户"],
        "数据中台": ["数据治理", "数据中台", "元数据", "数据目录", "数据交换", "数据质量", "ETL", "数据资产"],
        "政务服务": ["政务服务", "行政审批", "一网通办", "移动端", "流程优化", "办件", "电子证照"],
    }

    # 通用关键词
    COMMON_KEYWORDS = [
        "废标", "无效投标", "保证金", "签字盖章", "★", "实质性",
        "等保", "国产化", "信创", "CMMI", "ISO",
        "评分", "报价", "预算", "业绩", "资质",
    ]

    @staticmethod
    async def search(tender_text: str, project_type: str = "") -> list[KnowledgeRef]:
        """根据招标文件内容检索知识库"""
        refs = []
        kb_dir = Path(KNOWLEDGE_BASE_DIR)
        if not kb_dir.exists():
            return refs

        # 收集搜索关键词
        search_keywords = set(KnowledgeService.COMMON_KEYWORDS)
        if project_type and project_type in KnowledgeService.TYPE_KEYWORDS:
            search_keywords.update(KnowledgeService.TYPE_KEYWORDS[project_type])

        # 从文本中提取额外关键词
        for ptype, kws in KnowledgeService.TYPE_KEYWORDS.items():
            for kw in kws:
                if kw in tender_text:
                    search_keywords.update(kws)

        # 遍历知识库文件
        for f in sorted(kb_dir.iterdir()):
            if f.suffix != ".md":
                continue
            try:
                content = f.read_text(encoding="utf-8")
                # 检查关键词匹配
                matched_keywords = [kw for kw in search_keywords if kw in content]
                if not matched_keywords:
                    continue

                # 提取标题
                title = f.stem.replace("_", " ").title()
                for line in content.split("\n")[:3]:
                    if line.startswith("#"):
                        title = line.lstrip("# ").strip()
                        break

                # 提取相关片段
                snippets = []
                for line in content.split("\n"):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    for kw in matched_keywords:
                        if kw in line:
                            snippets.append(line[:200])
                            break
                    if len(snippets) >= 3:
                        break

                snippet = snippets[0] if snippets else content[:200]
                refs.append(KnowledgeRef(
                    source=f.name,
                    title=title,
                    snippet=snippet
                ))
            except Exception as e:
                logger.error(f"读取知识库文件失败 {f.name}: {e}")

        return refs

    @staticmethod
    def get_all_sources() -> list[dict]:
        """获取所有知识库文件信息"""
        kb_dir = Path(KNOWLEDGE_BASE_DIR)
        if not kb_dir.exists():
            return []
        results = []
        for f in sorted(kb_dir.iterdir()):
            if f.suffix == ".md":
                results.append({
                    "name": f.name,
                    "size": f.stat().st_size,
                })
        return results
