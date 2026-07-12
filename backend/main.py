"""BidPilot 后端主入口"""
import sys
import uuid
import logging
import re
from pathlib import Path

# Support both documented startup styles:
# 1. from project root: python -m uvicorn backend.main:app
# 2. from backend/: uvicorn main:app
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.config import (
    ANALYSIS_CACHE_MAX_ENTRIES,
    CORS_ORIGINS,
    MAX_UPLOAD_SIZE_BYTES,
    MOCK_MODE,
    OUTPUT_DIR,
    VERSION,
)
from backend.models.schemas import (
    HealthResult, AnalyzeRequest, ExportRequest,
    SolutionRequest, ResponseTableRequest, ComplianceCheckRequest,
    UploadResult, AnalysisResult,
)
from backend.services.mock_data_service import MockDataService
from backend.services.tender_service import tender_service
from backend.services.document_loader import DocumentLoader
from backend.services.export_service import ExportService

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BidPilot API",
    description="政企软件信息化投标智能Agent系统",
    version=VERSION,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    # BidPilot does not use browser cookies. Keeping this disabled makes a
    # wildcard public demo origin valid and avoids credential leakage.
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 上传文件临时目录
UPLOAD_DIR = Path(OUTPUT_DIR).parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 存储最近的分析结果
_analysis_cache: dict[str, AnalysisResult] = {}
UPLOAD_ID_PATTERN = re.compile(r"^upload_[0-9a-f]{8}$")


def _cache_result(result: AnalysisResult) -> None:
    """Keep in-memory analysis state bounded for long-running deployments."""
    _analysis_cache[result.task_id] = result
    while len(_analysis_cache) > ANALYSIS_CACHE_MAX_ENTRIES:
        _analysis_cache.pop(next(iter(_analysis_cache)))


def _uploaded_file_path(tender_id: str) -> Path:
    """Find exactly the file created for a server-issued upload identifier."""
    if not UPLOAD_ID_PATTERN.fullmatch(tender_id):
        raise HTTPException(status_code=404, detail="未找到上传文件")
    matches = list(UPLOAD_DIR.glob(f"{tender_id}.*"))
    if len(matches) != 1 or not matches[0].is_file():
        raise HTTPException(status_code=404, detail="未找到上传文件")
    return matches[0]


@app.get("/", include_in_schema=False)
async def root():
    """Space/root health entrypoint."""
    return {"name": "BidPilot API", "status": "ok", "docs": "/docs", "health": "/api/health"}


@app.get("/api/health", response_model=HealthResult)
async def health_check():
    """健康检查"""
    return HealthResult(status="ok", mock_mode=MOCK_MODE, version=VERSION)


@app.get("/api/sample-tenders")
async def list_sample_tenders():
    """获取示例招标文件列表"""
    return MockDataService.get_all()


@app.post("/api/tenders/upload", response_model=UploadResult)
async def upload_tender(file: UploadFile = File(...)):
    """上传招标文件"""
    try:
        # 检查文件格式
        ext = Path(file.filename or "").suffix.lower()
        if ext not in {".txt", ".md", ".docx", ".pdf"}:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件格式: {ext}，支持格式: .txt, .md, .docx, .pdf"
            )

        declared_size = file.size
        if declared_size is not None and declared_size > MAX_UPLOAD_SIZE_BYTES:
            raise HTTPException(status_code=413, detail=f"文件不能超过 {MAX_UPLOAD_SIZE_BYTES // (1024 * 1024)} MB")

        # 保存文件
        tender_id = f"upload_{uuid.uuid4().hex[:8]}"
        file_path = UPLOAD_DIR / f"{tender_id}{ext}"
        # Read one extra byte so clients without a Content-Length cannot
        # bypass the same server-side cap.
        content = await file.read(MAX_UPLOAD_SIZE_BYTES + 1)
        if len(content) > MAX_UPLOAD_SIZE_BYTES:
            raise HTTPException(status_code=413, detail=f"文件不能超过 {MAX_UPLOAD_SIZE_BYTES // (1024 * 1024)} MB")
        if not content:
            raise HTTPException(status_code=400, detail="上传文件不能为空")
        file_path.write_bytes(content)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("保存上传文件失败")
        raise HTTPException(status_code=500, detail="文件保存失败") from e
    finally:
        await file.close()

    return UploadResult(tender_id=tender_id, file_name=file.filename or "", status="uploaded")


@app.post("/api/tenders/analyze", response_model=AnalysisResult)
async def analyze_tender(req: AnalyzeRequest):
    """分析招标文件 - 核心API"""
    tender_id = req.tender_id

    # 如果是上传的文件，先加载内容
    tender_text = ""
    if tender_id.startswith("upload_"):
        uploaded_file = _uploaded_file_path(tender_id)
        tender_text = await DocumentLoader.load_from_upload(str(uploaded_file))
        if not tender_text:
            raise HTTPException(status_code=404, detail=f"未找到上传文件: {tender_id}")

    try:
        result = await tender_service.analyze(tender_id, tender_text)
        _cache_result(result)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"分析失败: {e}")
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@app.post("/api/bid/solution")
async def generate_solution(req: SolutionRequest):
    """生成技术方案"""
    result = _analysis_cache.get(req.task_id)
    if result:
        return {"solution": result.solution.model_dump()}
    # 如果没有缓存，重新分析
    if req.tender_id:
        try:
            result = await tender_service.analyze(req.tender_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        _cache_result(result)
        return {"solution": result.solution.model_dump()}
    raise HTTPException(status_code=404, detail="未找到分析结果，请先执行分析")


@app.post("/api/bid/response-table")
async def generate_response_table(req: ResponseTableRequest):
    """生成响应表"""
    result = _analysis_cache.get(req.task_id)
    if result:
        return {"response_tables": result.response_tables.model_dump()}
    if req.tender_id:
        try:
            result = await tender_service.analyze(req.tender_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        _cache_result(result)
        return {"response_tables": result.response_tables.model_dump()}
    raise HTTPException(status_code=404, detail="未找到分析结果，请先执行分析")


@app.post("/api/bid/compliance-check")
async def compliance_check(req: ComplianceCheckRequest):
    """合规审查"""
    result = _analysis_cache.get(req.task_id)
    if result:
        return {"compliance": result.compliance.model_dump()}
    if req.tender_id:
        try:
            result = await tender_service.analyze(req.tender_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        _cache_result(result)
        return {"compliance": result.compliance.model_dump()}
    raise HTTPException(status_code=404, detail="未找到分析结果，请先执行分析")


@app.post("/api/export/markdown")
async def export_markdown(req: ExportRequest):
    """导出Markdown报告"""
    result = _analysis_cache.get(req.task_id)
    if not result:
        raise HTTPException(status_code=404, detail="未找到分析结果，请先执行分析")

    try:
        exported = await ExportService.export_reports(req.task_id, result.reports.model_dump(), req.report_type)
        if not exported:
            raise HTTPException(status_code=404, detail=f"未找到匹配的报告类型: {req.report_type}")
        return {"status": "ok", "files": exported}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
