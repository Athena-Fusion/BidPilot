# BidPilot

> 面向政企软件信息化项目的智能投标 Agent 系统

## 项目简介

BidPilot 是一个面向政企软件、信息化项目招投标场景的行业 Agent 系统。它的核心不是通用文档问答，而是围绕投标业务闭环做结构化读标、风险识别、策略生成、响应表与标书初稿生成。

**一句话定位**：BidPilot 是面向政企软件信息化项目的智能投标Agent，能够从招标文件中自动提取关键要求、识别废标风险、分析评分规则，并生成投标策略、响应表、偏离表、技术方案和合规审查报告。

## 行业痛点

1. **读标慢**：一份100+页的招标文件，人工阅读需要2-4小时
2. **漏响应**：资格要求和★号参数容易遗漏，导致废标
3. **废标风险高**：报价超预算、保证金缺失、签章不规范等常见废标原因
4. **响应表耗时**：手动填写技术响应表和偏离表需要半天以上
5. **经验依赖**：新人投标需要老员工指导，效率低

## 解决方案

BidPilot 通过多 Agent 协作，将招标文件解析、资格要求提取、评分规则分析、废标风险识别、投标策略生成、响应表和偏离表生成、技术方案初稿、合规审查和报告导出串成一个完整业务闭环。

## 核心功能

| 功能 | 说明 |
|------|------|
| 招标解析 | 提取项目名称、预算、截止时间、保证金等基本信息 |
| 资格要求提取 | 识别资格条件、强制响应项，标注风险等级 |
| 评分规则分析 | 提取技术/商务/价格分，识别高权重项和★号参数 |
| 废标风险识别 | 覆盖报价、资质、签章、保证金、★号参数等常见废标风险 |
| 投标策略生成 | 综合评估是否建议投标，输出胜算评估和得分策略 |
| 技术方案初稿 | 生成13章节技术方案，强化高权重评分项 |
| 商务响应 | 逐条响应服务周期、付款方式、质保、知识产权等 |
| 响应表/偏离表 | 生成技术响应表、商务响应表，默认无负偏离 |
| 合规审查 | 检查资格覆盖、★号参数、保证金、签章等 |
| Markdown导出 | 导出完整投标分析报告 |

## 多 Agent 架构

```
TenderParserAgent  → 招标文件基本信息提取
RequirementAgent   → 资格要求提取与分析
ScoringAgent       → 评分规则提取与分析
RiskAgent          → 废标风险识别
StrategyAgent      → 投标策略生成
SolutionAgent      → 技术方案初稿生成
BusinessAgent      → 商务响应生成
ResponseTableAgent → 响应表/偏离表生成
ComplianceAgent    → 合规审查
ReportAgent        → 报告生成与导出
```

每个 Agent 有明确职责、输入、输出和可解释结果（agent_trace）。

## 业务闭环流程

```
选择示例招标文件
  → 一键分析
  → Agent 流程可视化
  → 招标摘要
  → 资格要求
  → 评分规则
  → 废标风险
  → 投标策略
  → 技术方案初稿
  → 商务响应
  → 响应表 / 偏离表
  → 合规审查
  → Markdown 导出
```

## 技术架构

```
frontend React/Vite/TypeScript/TailwindCSS
        |
        | REST API
        v
backend FastAPI/Python/Pydantic
        |
        +-- TenderService 编排 Agent
        +-- DocumentLoader 解析文件
        +-- KnowledgeService 检索本地知识库
        +-- ExportService 导出 Markdown
        |
        v
backend/agents 多 Agent
        |
        +-- BaseAgent + LLMClient
        +-- mock / openai-compatible / custom model
```

## 项目目录

```
BidPilot/
├── README.md
├── .env.example
├── docs/
│   ├── demo_script.md
│   ├── deployment_guide.md
│   ├── value_statement.md
│   ├── pitch_outline.md
│   └── ascend_npu_adaptation.md
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── tender_parser_agent.py
│   │   ├── requirement_agent.py
│   │   ├── scoring_agent.py
│   │   ├── risk_agent.py
│   │   ├── strategy_agent.py
│   │   ├── solution_agent.py
│   │   ├── business_agent.py
│   │   ├── response_table_agent.py
│   │   ├── compliance_agent.py
│   │   └── report_agent.py
│   ├── services/
│   │   ├── document_loader.py
│   │   ├── tender_service.py
│   │   ├── knowledge_service.py
│   │   ├── export_service.py
│   │   └── mock_data_service.py
│   ├── models/
│   │   └── schemas.py
│   ├── data/
│   │   ├── sample_tenders/       (3份模拟招标文件)
│   │   ├── knowledge_base/       (6份知识库Markdown)
│   │   └── outputs/              (导出报告)
│   └── tests/
├── frontend/
│   ├── package.json
│   ├── index.html
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── api/client.ts
│       ├── pages/               (6个页面)
│       ├── components/          (8个组件)
│       └── types/index.ts
└── examples/
    ├── demo_input.json
    └── demo_output.md
```

## 快速开始

### 后端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

如果 `python -m venv .venv` 提示 `ensurepip is not available` 或虚拟环境没有 `pip`，请先安装系统 `python3-venv` 后重新创建虚拟环境，详见 `docs/deployment_guide.md`。

### 前端

```bash
cd frontend
npm install
npm run dev
```

### 访问

- 前端：http://localhost:5173
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs

## 环境变量配置

复制 `.env.example` 为 `.env`，默认 `MOCK_MODE=true`，无需配置任何模型API即可完整演示。

| 变量 | 默认值 | 说明 |
|------|--------|------|
| MOCK_MODE | true | Mock演示模式 |
| OPENAI_COMPATIBLE_MODE | false | OpenAI兼容接口模式 |
| CUSTOM_MODEL_MODE | false | 自定义模型模式 |
| LLM_API_KEY | - | 模型API密钥 |
| LLM_BASE_URL | - | 模型API地址 |
| LLM_MODEL | deepseek-v4-flash | 模型名称 |

## Demo 演示流程

1. 打开 Dashboard，查看量化价值和示例项目
2. 选择"智慧园区综合管理平台建设项目"
3. 点击"一键分析"，观看 Agent 流程
4. 查看招标摘要、资格要求、评分规则
5. 切换到"风险审查"，查看高风险项
6. 切换到"投标策略"，查看建议和材料清单
7. 切换到"标书生成"，查看技术方案和响应表
8. 切换到"合规审查"，查看致命问题和免责声明
9. 点击"导出Markdown"

详细演示脚本见 [docs/demo_script.md](docs/demo_script.md)。

## 示例招标文件说明

| ID | 项目名称 | 预算 | 行业 | 特点 |
|----|----------|------|------|------|
| sample_001 | 智慧园区综合管理平台 | 480万 | 智慧园区 | ★号参数、国产化、数据安全 |
| sample_002 | 区级数据中台 | 800万 | 数据中台 | 数据治理、等保三级、接口标准 |
| sample_003 | 政务服务一体化平台升级 | 350万 | 政务服务 | 移动端、流程优化、培训运维 |

## 输出结果示例

详见 [examples/demo_output.md](examples/demo_output.md)。

## 量化价值说明（基于模拟案例估算）

| 工作项 | 传统方式 | BidPilot辅助 | 提升幅度 |
|--------|----------|-------------|---------|
| 初步读标 | 2-4小时 | 10-20分钟 | 约90%↓ |
| 资格要求整理 | 1小时 | 5分钟 | 约92%↓ |
| 评分点分析 | 1-2小时 | 10分钟 | 约88%↓ |
| 响应表初稿 | 半天 | 10-15分钟 | 约93%↓ |
| 废标风险检查 | 依赖经验 | 自动覆盖 | 覆盖度↑ |

## 比赛评分点对应说明

| 评分维度 | BidPilot 对应 |
|----------|--------------|
| 技术创新性 | 多Agent协作、结构化解析、知识库检索、风险识别、模型调用抽象 |
| 场景落地性 | 解决读标慢、漏响应、废标风险高，政企信息化投标垂直场景 |
| 作品完整性 | 前端+后端+Agent+示例文件+报告+文档，Mock模式开箱可演示 |
| UI/UX | 文件选择、Agent流程可视化、风险标签、报告导出，企业级工作台 |
| 答辩表现 | 行业痛点、业务闭环、量化价值、扩展路线 |

## 项目规范

- 贡献指南：[CONTRIBUTING.md](CONTRIBUTING.md)
- 安全说明：[SECURITY.md](SECURITY.md)
- 行为准则：[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- 许可证：[MIT License](LICENSE)

BidPilot 的产品方向是成为合规、可复核、可落地的政企软件投标辅助工作台。项目不追求替代人工判断，也不提供任何不正当竞争建议。

## 未来扩展方向

1. 真实大语言模型接入（OpenAI Compatible / 自定义模型）
2. 向量检索 RAG 知识库
3. .docx 标书导出
4. 企业资质材料库
5. 多项目历史记录
6. 扫描件/图片型PDF解析
7. Docker 容器化部署
8. 昇腾 NPU 适配与模型部署

## 免责声明

1. BidPilot 输出仅作为投标辅助参考，不构成法律、财务或最终投标意见。
2. 所有合规结论标注"辅助审查，需人工复核"。
3. 不伪造企业资质、业绩、证书或人员信息。
4. 不确定内容标注"需人工确认"。
5. 不生成围标、串标、控标或不正当竞争建议。
6. 示例数据均为虚构，仅用于演示。
7. 量化价值基于模拟案例估算，不代表实际使用效果。
