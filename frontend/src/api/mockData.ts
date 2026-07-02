import type { AnalysisResult, HealthResult, SampleTender } from '../types';

export const mockHealth: HealthResult = {
  status: 'ok',
  mock_mode: true,
  version: '0.1.0-static',
};

export const mockSampleTenders: SampleTender[] = [
  {
    id: 'sample_001',
    name: '某市智慧园区综合管理平台建设项目',
    file_name: 'sample_tender_001_smart_park.md',
    budget: '480万元',
    industry: '智慧园区',
    description: '覆盖统一门户、设备接入、数据可视化、国产化适配和数据安全要求',
  },
  {
    id: 'sample_002',
    name: '某区数据中台建设项目',
    file_name: 'sample_tender_002_data_platform.md',
    budget: '800万元',
    industry: '数据中台',
    description: '覆盖数据治理、数据目录、数据交换、数据质量、等保和接口标准',
  },
  {
    id: 'sample_003',
    name: '某市政务服务一体化平台升级项目',
    file_name: 'sample_tender_003_government_service.md',
    budget: '350万元',
    industry: '政务服务',
    description: '覆盖移动端适配、流程优化、用户体验、培训和售后服务',
  },
];

const tenderProfiles: Record<string, Pick<SampleTender, 'name' | 'budget' | 'industry'>> = Object.fromEntries(
  mockSampleTenders.map((sample) => [sample.id, sample]),
);

function profileFor(tenderId: string) {
  return tenderProfiles[tenderId] ?? tenderProfiles.sample_001;
}

export function getMockAnalysisResult(tenderId: string): AnalysisResult {
  const profile = profileFor(tenderId);
  const taskId = `static_${tenderId.replace(/[^a-z0-9_]/gi, '').slice(0, 20) || 'analysis'}`;

  return {
    task_id: taskId,
    tender_id: tenderId,
    tender_name: profile.name,
    mode: 'static-mock',
    basic_info: {
      project_name: profile.name,
      buyer: profile.industry === '数据中台' ? '某区大数据管理局' : profile.industry === '政务服务' ? '某市行政审批局' : '某市大数据中心',
      budget: profile.budget,
      deadline: '2026年7月15日 09:30',
      service_period: profile.industry === '数据中台' ? '合同签订后120日内完成建设' : profile.industry === '政务服务' ? '合同签订后60日内完成升级' : '合同签订后90日内完成建设并上线试运行',
      delivery_location: '采购人指定地点',
      bid_bond: profile.industry === '数据中台' ? '8万元' : profile.industry === '政务服务' ? '3万元' : '5万元',
      procurement_scope: `${profile.industry}平台建设、实施、培训、运维及验收支持`,
      project_type: profile.industry,
    },
    requirements: [
      { requirement: '具备有效营业执照和履约能力证明', type: '资格要求', mandatory: true, risk_level: 'low', suggestion: '确认主体资质、经营范围和授权链路。' },
      { requirement: '提供近三年同类信息化项目业绩证明', type: '业绩要求', mandatory: true, risk_level: 'high', suggestion: '准备合同关键页、验收材料和客户证明。' },
      { requirement: '项目经理具备 PMP 或信息系统项目管理师证书', type: '人员要求', mandatory: true, risk_level: 'medium', suggestion: '核验证书有效期及社保证明。' },
      { requirement: '投标文件须按要求签字盖章并提交保证金凭证', type: '格式要求', mandatory: true, risk_level: 'high', suggestion: '建立提交前逐页检查清单。' },
    ],
    scoring: {
      total_score: 100,
      technical_score: profile.industry === '数据中台' ? 65 : 60,
      business_score: 20,
      price_score: profile.industry === '数据中台' ? 15 : 20,
      strategy_summary: '技术方案与实质性条款响应是主要得分点，商务材料完整性决定废标风险。',
      items: [
        { item: '总体架构设计', score: 10, weight: '高', description: '架构完整性、可扩展性、可靠性', strategy: '突出分层架构、可观测性和部署落地。' },
        { item: `${profile.industry}核心功能方案`, score: 15, weight: '高', description: '核心业务功能覆盖度', strategy: '逐条响应功能要求，给出可验收指标。' },
        { item: '安全与国产化适配', score: 10, weight: '高', description: '等保、国密、信创适配', strategy: '列出适配清单和测试方法。' },
        { item: '实施计划与服务保障', score: 8, weight: '中', description: '里程碑、团队、培训和售后', strategy: '用阶段计划绑定交付物。' },
      ],
      high_value_items: [
        { item: `${profile.industry}核心功能方案`, score: 15, weight: '高', description: '核心业务功能覆盖度', strategy: '逐条响应功能要求，给出可验收指标。' },
        { item: '总体架构设计', score: 10, weight: '高', description: '架构完整性、可扩展性、可靠性', strategy: '突出分层架构、可观测性和部署落地。' },
        { item: '安全与国产化适配', score: 10, weight: '高', description: '等保、国密、信创适配', strategy: '列出适配清单和测试方法。' },
      ],
    },
    risks: [
      { risk: `投标报价不得超过采购预算 ${profile.budget}`, risk_type: '价格废标风险', severity: 'high', evidence: '预算金额为最高限价', action: '报价测算必须保留复核记录。' },
      { risk: '投标保证金、签字盖章、文件格式缺失将导致废标', risk_type: '格式风险', severity: 'high', evidence: '形式审查为前置条件', action: '提交前执行双人核验。' },
      { risk: '同类业绩证明材料可能不完整', risk_type: '资格废标风险', severity: 'medium', evidence: '业绩通常要求合同与验收材料', action: '补齐关键页和验收证明。' },
      { risk: '技术方案中的不确定参数需要人工确认', risk_type: '技术风险', severity: 'medium', evidence: '部分技术选型依赖现网环境', action: '在方案中标注确认项并准备答疑问题。' },
      { risk: '培训、运维响应承诺需要与服务团队能力匹配', risk_type: '商务风险', severity: 'low', evidence: '服务条款影响履约', action: '确认服务排班和响应机制。' },
    ],
    strategy: {
      recommendation: '谨慎参与',
      win_assessment: '技术分占比较高，若能完整响应核心功能、国产化适配和安全要求，则具备较好竞争空间。',
      score_strategy: [
        `围绕${profile.industry}核心场景组织技术方案，避免只堆通用能力。`,
        '高权重评分项逐条建立“要求-响应-证明材料-验收指标”链路。',
        '价格控制在预算以内，同时保留实施、培训和运维成本空间。',
        '所有资质、业绩、人员、保证金和签章材料在提交前双人复核。',
      ],
      price_suggestion: `报价须低于 ${profile.budget}，建议结合实施工作量、运维承诺和同类项目价格测算，不生成任何不正当竞争建议。`,
      material_checklist: ['营业执照副本', '近三年审计或财务证明', '同类项目合同及验收材料', '项目经理证书和社保证明', '投标保证金凭证', '签字盖章检查清单'],
      management_summary: `本项目为${profile.industry}类政企信息化项目，建议在材料完备、技术响应可落地的前提下参与。高风险主要集中在价格上限、格式合规和证明材料完整性。`,
    },
    solution: {
      toc: ['1. 项目理解与需求分析', '2. 总体架构设计', '3. 核心功能方案', '4. 安全与国产化适配', '5. 实施与运维计划'],
      total_words: 620,
      sections: [
        { title: '1. 项目理解与需求分析', content: `本项目围绕${profile.industry}场景建设，目标是提升数据汇聚、业务协同、可视化管理和安全运维能力。方案应以招标文件实质性要求为主线，逐项形成可验收响应。`, needs_review: false },
        { title: '2. 总体架构设计', content: '建议采用展示层、业务服务层、数据服务层、基础支撑层的分层架构，并配置统一认证、日志审计、权限控制和接口网关。具体技术选型需结合投标单位既有能力确认。', needs_review: true },
        { title: '3. 核心功能方案', content: `围绕${profile.industry}核心业务，提供事项管理、数据接入、统计分析、流程协同、报表导出、移动适配和可视化驾驶舱等能力。`, needs_review: true },
        { title: '4. 安全与国产化适配', content: '覆盖等保要求、数据加密、敏感信息脱敏、操作审计、备份恢复，以及国产 CPU、操作系统、数据库和中间件适配验证。', needs_review: false },
        { title: '5. 实施与运维计划', content: '按需求确认、设计开发、联调测试、培训上线、验收移交组织里程碑，并明确项目团队、周报机制、风险台账和售后响应承诺。', needs_review: true },
      ],
    },
    business_response: {
      summary: '商务条款默认按完全响应组织，所有金额、期限和服务承诺需由投标负责人最终确认。',
      items: [
        { clause: '服务周期', requirement: '按招标文件约定期限完成交付', response: '完全响应，并提交里程碑实施计划。', needs_review: true },
        { clause: '质保与运维', requirement: '提供质保期和响应服务', response: '完全响应，提供热线、远程和现场支持。', needs_review: true },
        { clause: '付款条件', requirement: '按合同节点付款', response: '完全响应采购人付款安排。', needs_review: true },
      ],
    },
    response_tables: {
      technical_response: [
        { id: 1, tender_requirement: `${profile.industry}平台建设及核心功能覆盖`, response: '完全响应，详见技术方案核心功能章节。', deviation: '无偏离', proof: '技术方案、实施计划', risk_level: 'medium' },
        { id: 2, tender_requirement: '安全、审计和权限控制要求', response: '完全响应，提供等保、审计、权限和数据安全设计。', deviation: '无偏离', proof: '安全设计章节', risk_level: 'low' },
        { id: 3, tender_requirement: '国产化适配要求', response: '完全响应，按 CPU、操作系统、数据库和中间件逐项验证。', deviation: '无偏离', proof: '适配测试报告', risk_level: 'medium' },
      ],
      business_response: [
        { id: 1, tender_requirement: '按期交付和验收', response: '完全响应，提交里程碑计划和验收清单。', deviation: '无偏离', proof: '项目计划', risk_level: 'low' },
      ],
      technical_deviation: [],
      business_deviation: [],
    },
    compliance: {
      overall_status: '存在高风险，需补齐材料后复核',
      pass_rate: '82%',
      critical_issues: [
        { item: '报价上限', status: '待复核', severity: 'high', suggestion: `最终报价必须小于等于 ${profile.budget}。` },
        { item: '保证金与签章', status: '待复核', severity: 'high', suggestion: '提交前核验保证金凭证、签字盖章和文件格式。' },
      ],
      warnings: [
        { item: '业绩证明', status: '待补充', severity: 'medium', suggestion: '补齐合同关键页、验收材料和客户证明。' },
        { item: '技术参数', status: '需确认', severity: 'medium', suggestion: '对需人工确认项完成内部技术复核。' },
      ],
      manual_review_items: ['报价测算', '业绩材料真实性', '项目经理资质和社保', '国产化适配承诺', '售后服务排班'],
      suggestions: ['建立投标文件提交清单', '将评分项映射到方案目录', '由法务复核合同和商务偏离表'],
      disclaimer: '本报告由 BidPilot 自动生成，仅用于投标准备辅助。招标文件解释、投标文件最终内容、报价和合规判断均需由投标负责人、法务或专业人员人工复核确认。',
    },
    reports: {
      files: [
        {
          name: 'tender_analysis_report.md',
          content: `# 招标分析报告 - ${profile.name}\n\n预算：${profile.budget}\n\n## 投标建议\n谨慎参与，先补齐关键证明材料并复核报价上限。\n`,
        },
        {
          name: 'risk_checklist.md',
          content: `# 风险检查清单 - ${profile.name}\n\n- 报价不得超过 ${profile.budget}\n- 保证金、签章、格式需双人复核\n- 业绩材料需补齐合同和验收证明\n`,
        },
      ],
    },
    agent_trace: [
      { agent: 'TenderParserAgent', status: 'completed', summary: '提取项目基本信息', duration_ms: 120, references: [] },
      { agent: 'RequirementAgent', status: 'completed', summary: '识别资格与格式要求', duration_ms: 110, references: ['compliance_checklist.md'] },
      { agent: 'ScoringAgent', status: 'completed', summary: '解析评分结构和高权重项', duration_ms: 100, references: ['common_scoring_rules.md'] },
      { agent: 'RiskAgent', status: 'completed', summary: '识别价格、格式、资格和技术风险', duration_ms: 130, references: ['invalid_bid_risk_rules.md'] },
      { agent: 'ReportAgent', status: 'completed', summary: '生成演示报告', duration_ms: 90, references: [] },
    ],
    knowledge_refs: [
      { source: 'knowledge_base', title: '废标风险规则', snippet: '报价、保证金、签章、资质和实质性条款为高优先级复核项。' },
      { source: 'knowledge_base', title: '评分响应规则', snippet: '高权重评分项应形成要求、响应、证明材料、验收指标闭环。' },
    ],
  };
}

export function getMockUploadResult(fileName: string) {
  return {
    tender_id: 'upload_static_demo',
    file_name: fileName,
    status: 'uploaded',
  };
}
