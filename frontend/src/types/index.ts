// BidPilot 前端类型定义

export interface BasicInfo {
  project_name: string;
  buyer: string;
  budget: string;
  deadline: string;
  service_period: string;
  delivery_location: string;
  bid_bond: string;
  procurement_scope: string;
  project_type: string;
}

export interface RequirementItem {
  requirement: string;
  type: string;
  mandatory: boolean;
  risk_level: string;
  suggestion: string;
}

export interface ScoringItem {
  item: string;
  score: number;
  weight: string;
  description: string;
  strategy: string;
}

export interface ScoringResult {
  total_score: number;
  technical_score: number;
  business_score: number;
  price_score: number;
  items: ScoringItem[];
  high_value_items: ScoringItem[];
  strategy_summary: string;
}

export interface RiskItem {
  risk: string;
  risk_type: string;
  severity: string;
  evidence: string;
  action: string;
}

export interface StrategyResult {
  recommendation: string;
  win_assessment: string;
  score_strategy: string[];
  price_suggestion: string;
  material_checklist: string[];
  management_summary: string;
}

export interface SolutionSection {
  title: string;
  content: string;
  needs_review: boolean;
}

export interface SolutionResult {
  sections: SolutionSection[];
  toc: string[];
  total_words: number;
}

export interface BusinessItem {
  clause: string;
  requirement: string;
  response: string;
  needs_review: boolean;
}

export interface BusinessResponse {
  items: BusinessItem[];
  summary: string;
}

export interface ResponseTableRow {
  id: number;
  tender_requirement: string;
  response: string;
  deviation: string;
  proof: string;
  risk_level: string;
}

export interface ResponseTables {
  technical_response: ResponseTableRow[];
  business_response: ResponseTableRow[];
  technical_deviation: ResponseTableRow[];
  business_deviation: ResponseTableRow[];
}

export interface ComplianceIssue {
  item: string;
  status: string;
  severity: string;
  suggestion: string;
}

export interface ComplianceResult {
  overall_status: string;
  pass_rate: string;
  critical_issues: ComplianceIssue[];
  warnings: ComplianceIssue[];
  manual_review_items: string[];
  suggestions: string[];
  disclaimer: string;
}

export interface ReportFile {
  name: string;
  content: string;
}

export interface Reports {
  files: ReportFile[];
}

export interface AgentTrace {
  agent: string;
  status: string;
  summary: string;
  duration_ms: number;
  references: string[];
}

export interface KnowledgeRef {
  source: string;
  title: string;
  snippet: string;
}

export interface AnalysisResult {
  task_id: string;
  tender_id: string;
  tender_name: string;
  mode: string;
  basic_info: BasicInfo;
  requirements: RequirementItem[];
  scoring: ScoringResult;
  risks: RiskItem[];
  strategy: StrategyResult;
  solution: SolutionResult;
  business_response: BusinessResponse;
  response_tables: ResponseTables;
  compliance: ComplianceResult;
  reports: Reports;
  agent_trace: AgentTrace[];
  knowledge_refs: KnowledgeRef[];
}

export interface SampleTender {
  id: string;
  name: string;
  file_name: string;
  budget: string;
  industry: string;
  description: string;
}

export interface HealthResult {
  status: string;
  mock_mode: boolean;
  version: string;
}
