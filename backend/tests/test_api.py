"""BidPilot 后端测试"""
import pytest
from httpx import AsyncClient, ASGITransport
from backend import main as main_module
from backend.main import app
from backend.services.export_service import ExportService


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["mock_mode"] is True


@pytest.mark.anyio
async def test_sample_tenders():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/api/sample-tenders")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 3
        assert data[0]["id"] == "sample_001"


@pytest.mark.anyio
async def test_analyze():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/api/tenders/analyze", json={"tender_id": "sample_001"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["task_id"].startswith("analysis_")
        assert data["tender_id"] == "sample_001"
        assert data["mode"] == "mock"
        assert len(data["agent_trace"]) == 10
        assert data["basic_info"]["project_name"] != ""
        assert len(data["risks"]) > 0
        assert len(data["requirements"]) > 0
        assert len(data["reports"]["files"]) == 8
        assert "technical_response_table.md" in [f["name"] for f in data["reports"]["files"]]
        assert "deviation_table.md" in [f["name"] for f in data["reports"]["files"]]

        export_resp = await ac.post("/api/export/markdown", json={"task_id": data["task_id"], "report_type": "technical_response_table"})
        assert export_resp.status_code == 200
        exported = export_resp.json()
        assert [f["name"] for f in exported["files"]] == ["technical_response_table.md"]

        missing_report_resp = await ac.post("/api/export/markdown", json={"task_id": data["task_id"], "report_type": "missing_report"})
        assert missing_report_resp.status_code == 404


@pytest.mark.anyio
async def test_unknown_sample_returns_404():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/api/tenders/analyze", json={"tender_id": "sample_missing"})
        assert resp.status_code == 404


@pytest.mark.anyio
async def test_upload_and_analyze_text_tender():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        upload = await ac.post(
            "/api/tenders/upload",
            files={"file": ("tender.txt", "项目名称：上传测试项目\n采购人：测试单位", "text/plain")},
        )
        assert upload.status_code == 200
        tender_id = upload.json()["tender_id"]
        assert tender_id.startswith("upload_")

        analysis = await ac.post("/api/tenders/analyze", json={"tender_id": tender_id})
        assert analysis.status_code == 200
        assert analysis.json()["tender_id"] == tender_id


@pytest.mark.anyio
async def test_upload_rejects_empty_file_and_ambiguous_id():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        empty_upload = await ac.post(
            "/api/tenders/upload",
            files={"file": ("empty.txt", b"", "text/plain")},
        )
        assert empty_upload.status_code == 400

        ambiguous_id = await ac.post("/api/tenders/analyze", json={"tender_id": "upload_"})
        assert ambiguous_id.status_code == 404


@pytest.mark.anyio
async def test_upload_rejects_files_over_configured_limit(monkeypatch):
    monkeypatch.setattr(main_module, "MAX_UPLOAD_SIZE_BYTES", 4)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        upload = await ac.post(
            "/api/tenders/upload",
            files={"file": ("large.txt", b"12345", "text/plain")},
        )
        assert upload.status_code == 413


def test_export_only_accepts_plain_markdown_filenames():
    assert ExportService._safe_report_name("analysis.md") == "analysis.md"
    assert ExportService._safe_report_name("../analysis.md") is None
    assert ExportService._safe_report_name("analysis.txt") is None
