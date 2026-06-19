# Contributing to BidPilot

感谢关注 BidPilot。这个项目聚焦政企软件信息化投标场景，贡献应优先服务于真实、合规、可复核的投标准备流程。

## 开发原则

1. 默认保持 `MOCK_MODE=true`，确保无模型 API 时可完整演示。
2. 不提交真实敏感招标文件、企业资质、证书、人员信息或客户资料。
3. 不生成围标、串标、控标、不正当竞争或规避监管的功能和文案。
4. 不确定内容必须标注“需人工确认”。
5. 合规审查输出必须说明“辅助审查，需人工复核”。

## 本地验证

后端：

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests
```

前端：

```bash
cd frontend
npm install
npm run build
```

## 提交规范

- 保持改动聚焦，不混入无关重构。
- 不提交 `node_modules/`、`dist/`、`.venv/`、`__pycache__/`、导出报告等运行产物。
- 新增 Agent、API 或报告字段时，同步更新前端类型和 README。
