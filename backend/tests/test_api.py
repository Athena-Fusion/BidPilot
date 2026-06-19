"""BidPilot 后端测试"""
import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app


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
