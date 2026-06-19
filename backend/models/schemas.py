"""BidPilot 数据模型定义"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class RiskLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RiskType(str, Enum):
    PRICE = "价格废标风险"
    QUALIFICATION = "资格废标风险"
    TECHNICAL = "技术风险"
    COMMERCIAL = "商务风险"
    COMPLIANCE = "合规风险"
    FORMAT = "格式风险"


# === 基本信息 ===
class BasicInfo(BaseModel):
    project_name: str = ""
    buyer: str = ""
    budget: str = ""
    deadline: str = ""
    service_period: str = ""
    delivery_location: str = ""
    bid_bond: str = ""
    procurement_scope: str = ""
    project_type: str = ""


# === 资格要求 ===
class RequirementItem(BaseModel):
    requirement: str
    type: str = ""
    mandatory: bool = False
    risk_level: str = "low"
    suggestion: str = ""


# === 评分规则 ===
class ScoringItem(BaseModel):
    item: str
    score: float = 0
    weight: str = ""
    description: str = ""
    strategy: str = ""


class ScoringResult(BaseModel):
    total_score: float = 100
    technical_score: float = 0
    business_score: float = 0
    price_score: float = 0
    items: list[ScoringItem] = Field(default_factory=list)
    high_value_items: list[ScoringItem] = Field(default_factory=list)
    strategy_summary: str = ""


# === 风险 ===
class RiskItem(BaseModel):
    risk: str
    risk_type: str = ""
    severity: str = "medium"
    evidence: str = ""
    action: str = ""


# === 投标策略 ===
class StrategyResult(BaseModel):
    recommendation: str = ""
    win_assessment: str = ""
    score_strategy: list[str] = Field(default_factory=list)
    price_suggestion: str = ""
    material_checklist: list[str] = Field(default_factory=list)
    management_summary: str = ""


# === 技术方案 ===
class SolutionSection(BaseModel):
    title: str
    content: str
    needs_review: bool = False


class SolutionResult(BaseModel):
    sections: list[SolutionSection] = Field(default_factory=list)
    toc: list[str] = Field(default_factory=list)
    total_words: int = 0


# === 商务响应 ===
class BusinessItem(BaseModel):
    clause: str
    requirement: str
    response: str
    needs_review: bool = False


class BusinessResponse(BaseModel):
    items: list[BusinessItem] = Field(default_factory=list)
    summary: str = ""


# === 响应表 ===
class ResponseTableRow(BaseModel):
    id: int = 0
    tender_requirement: str = ""
    response: str = ""
    deviation: str = ""
    proof: str = ""
    risk_level: str = "low"


class ResponseTables(BaseModel):
    technical_response: list[ResponseTableRow] = Field(default_factory=list)
    business_response: list[ResponseTableRow] = Field(default_factory=list)
    technical_deviation: list[ResponseTableRow] = Field(default_factory=list)
    business_deviation: list[ResponseTableRow] = Field(default_factory=list)


# === 合规审查 ===
class ComplianceIssue(BaseModel):
    item: str
    status: str = ""
    severity: str = "medium"
    suggestion: str = ""


class ComplianceResult(BaseModel):
    overall_status: str = "需要人工复核"
    pass_rate: str = ""
    critical_issues: list[ComplianceIssue] = Field(default_factory=list)
    warnings: list[ComplianceIssue] = Field(default_factory=list)
    manual_review_items: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    disclaimer: str = "本报告由 BidPilot 自动生成，仅用于投标准备辅助。招标文件解释、投标文件最终内容、报价和合规判断均需由投标负责人、法务或专业人员人工复核确认。"


# === 报告 ===
class ReportFile(BaseModel):
    name: str
    content: str


class Reports(BaseModel):
    files: list[ReportFile] = Field(default_factory=list)


# === Agent Trace ===
class AgentTrace(BaseModel):
    agent: str
    status: str = "completed"
    summary: str = ""
    duration_ms: int = 0
    references: list[str] = Field(default_factory=list)


# === 知识库引用 ===
class KnowledgeRef(BaseModel):
    source: str
    title: str
    snippet: str


# === 完整分析结果 ===
class AnalysisResult(BaseModel):
    task_id: str = ""
    tender_id: str = ""
    tender_name: str = ""
    mode: str = "mock"
    basic_info: BasicInfo = Field(default_factory=BasicInfo)
    requirements: list[RequirementItem] = Field(default_factory=list)
    scoring: ScoringResult = Field(default_factory=ScoringResult)
    risks: list[RiskItem] = Field(default_factory=list)
    strategy: StrategyResult = Field(default_factory=StrategyResult)
    solution: SolutionResult = Field(default_factory=SolutionResult)
    business_response: BusinessResponse = Field(default_factory=BusinessResponse)
    response_tables: ResponseTables = Field(default_factory=ResponseTables)
    compliance: ComplianceResult = Field(default_factory=ComplianceResult)
    reports: Reports = Field(default_factory=Reports)
    agent_trace: list[AgentTrace] = Field(default_factory=list)
    knowledge_refs: list[KnowledgeRef] = Field(default_factory=list)


# === API 请求模型 ===
class AnalyzeRequest(BaseModel):
    tender_id: str = ""


class ExportRequest(BaseModel):
    task_id: str = ""
    report_type: str = "all"


class SolutionRequest(BaseModel):
    tender_id: str = ""
    task_id: str = ""


class ResponseTableRequest(BaseModel):
    tender_id: str = ""
    task_id: str = ""


class ComplianceCheckRequest(BaseModel):
    tender_id: str = ""
    task_id: str = ""


# === 示例招标文件信息 ===
class SampleTender(BaseModel):
    id: str
    name: str
    file_name: str
    budget: str
    industry: str
    description: str


# === 上传结果 ===
class UploadResult(BaseModel):
    tender_id: str
    file_name: str
    status: str = "uploaded"


# === 健康检查 ===
class HealthResult(BaseModel):
    status: str = "ok"
    mock_mode: bool = True
    version: str = "0.1.0"
