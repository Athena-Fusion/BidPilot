"""MockDataService - Mock数据服务"""
from backend.models.schemas import SampleTender


class MockDataService:
    """示例招标文件元数据"""

    SAMPLE_TENDERS = [
        SampleTender(
            id="sample_001",
            name="某市智慧园区综合管理平台建设项目",
            file_name="sample_tender_001_smart_park.md",
            budget="480万元",
            industry="智慧园区",
            description="覆盖统一门户、设备接入、数据可视化、国产化适配和数据安全要求"
        ),
        SampleTender(
            id="sample_002",
            name="某区数据中台建设项目",
            file_name="sample_tender_002_data_platform.md",
            budget="800万元",
            industry="数据中台",
            description="覆盖数据治理、数据目录、数据交换、数据质量、等保和接口标准"
        ),
        SampleTender(
            id="sample_003",
            name="某市政务服务一体化平台升级项目",
            file_name="sample_tender_003_government_service.md",
            budget="350万元",
            industry="政务服务",
            description="覆盖移动端适配、流程优化、用户体验、培训和售后服务"
        ),
    ]

    @staticmethod
    def get_all() -> list[SampleTender]:
        return MockDataService.SAMPLE_TENDERS

    @staticmethod
    def get_by_id(tender_id: str) -> SampleTender | None:
        for t in MockDataService.SAMPLE_TENDERS:
            if t.id == tender_id:
                return t
        return None
