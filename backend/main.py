"""BidPilot 后端主入口"""
import os
import sys
import uuid
import logging
from pathlib import Path

# Support both documented startup styles:
# 1. from project root: python -m uvicorn backend.main:app
# 2. from backend/: uvicorn main:app
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.config import MOCK_MODE, VERSION, OUTPUT_DIR
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 上传文件临时目录
UPLOAD_DIR = Path(OUTPUT_DIR).parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 存储最近的分析结果
_analysis_cache: dict[str, AnalysisResult] = {}


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
    # 检查文件格式
    ext = Path(file.filename or "").suffix.lower()
    if ext not in {".txt", ".md", ".docx", ".pdf"}:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式: {ext}，支持格式: .txt, .md, .docx, .pdf"
        )

    # 保存文件
    tender_id = f"upload_{uuid.uuid4().hex[:8]}"
    file_path = UPLOAD_DIR / f"{tender_id}{ext}"
    try:
        content = await file.read()
        file_path.write_bytes(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")

    return UploadResult(tender_id=tender_id, file_name=file.filename or "", status="uploaded")


@app.post("/api/tenders/analyze", response_model=AnalysisResult)
async def analyze_tender(req: AnalyzeRequest):
    """分析招标文件 - 核心API"""
    tender_id = req.tender_id

    # 如果是上传的文件，先加载内容
    tender_text = ""
    if tender_id.startswith("upload_"):
        upload_dir = UPLOAD_DIR
        for f in upload_dir.iterdir():
            if f.name.startswith(tender_id):
                tender_text = await DocumentLoader.load_from_upload(str(f))
                break
        if not tender_text:
            raise HTTPException(status_code=404, detail=f"未找到上传文件: {tender_id}")

    try:
        result = await tender_service.analyze(tender_id, tender_text)
        _analysis_cache[result.task_id] = result
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
        result = await tender_service.analyze(req.tender_id)
        _analysis_cache[result.task_id] = result
        return {"solution": result.solution.model_dump()}
    raise HTTPException(status_code=404, detail="未找到分析结果，请先执行分析")


@app.post("/api/bid/response-table")
async def generate_response_table(req: ResponseTableRequest):
    """生成响应表"""
    result = _analysis_cache.get(req.task_id)
    if result:
        return {"response_tables": result.response_tables.model_dump()}
    if req.tender_id:
        result = await tender_service.analyze(req.tender_id)
        _analysis_cache[result.task_id] = result
        return {"response_tables": result.response_tables.model_dump()}
    raise HTTPException(status_code=404, detail="未找到分析结果，请先执行分析")


@app.post("/api/bid/compliance-check")
async def compliance_check(req: ComplianceCheckRequest):
    """合规审查"""
    result = _analysis_cache.get(req.task_id)
    if result:
        return {"compliance": result.compliance.model_dump()}
    if req.tender_id:
        result = await tender_service.analyze(req.tender_id)
        _analysis_cache[result.task_id] = result
        return {"compliance": result.compliance.model_dump()}
    raise HTTPException(status_code=404, detail="未找到分析结果，请先执行分析")


@app.post("/api/export/markdown")
async def export_markdown(req: ExportRequest):
    """导出Markdown报告"""
    result = _analysis_cache.get(req.task_id)
    if not result:
        raise HTTPException(status_code=404, detail="未找到分析结果，请先执行分析")

    try:
        exported = await ExportService.export_reports(req.task_id, result.reports.model_dump())
        return {"status": "ok", "files": exported}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
