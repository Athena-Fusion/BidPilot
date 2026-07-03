# BidPilot 部署指南

## 环境要求

- Python 3.10+
- Node.js 24+（Vite 8 要求 Node `^20.19.0 || >=22.12.0`，推荐与 CI 保持 Node 24）
- npm 9+

## 后端部署

### 1. 创建虚拟环境

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows
```

如果在 Ubuntu/Debian 环境中出现 `ensurepip is not available` 或虚拟环境中没有 `pip`，先安装系统 venv 支持后重新创建：

```bash
sudo apt install python3-venv
cd backend
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp ../.env.example ../.env
# 默认 MOCK_MODE=true，无需配置模型API
```

### 4. 启动服务

```bash
uvicorn main:app --reload --port 8000
```

### 5. 验证

```bash
curl http://localhost:8000/api/health
# 返回 {"status":"ok","mock_mode":true,"version":"0.1.0"}
```

## 前端部署

### 1. 安装依赖

```bash
cd frontend
npm install
```

生产构建默认使用内置静态 Mock 数据，适合 GitHub Pages 纯静态演示。如果要连接真实后端，在构建前设置：

```bash
VITE_API_BASE_URL=https://your-api.example.com/api
```

当前 GitHub Pages workflow 已连接 Hugging Face Space 后端：

```text
https://jiehu-claire-bidpilot-api.hf.space/api
```

### 2. 开发模式启动

```bash
npm run dev
```

访问 http://localhost:5173

### 3. 生产构建

```bash
npm run build
```

构建产物在 `dist/` 目录。

## 环境变量说明

| 变量 | 默认值 | 说明 |
|------|--------|------|
| MOCK_MODE | true | Mock演示模式，无需模型API |
| OPENAI_COMPATIBLE_MODE | false | OpenAI兼容接口模式 |
| CUSTOM_MODEL_MODE | false | 自定义模型模式 |
| LLM_API_KEY | - | 模型API密钥 |
| LLM_BASE_URL | - | 模型API地址 |
| LLM_MODEL | deepseek-v4-flash | 模型名称 |
| BACKEND_HOST | 0.0.0.0 | 后端监听地址 |
| BACKEND_PORT | 8000 | 后端监听端口 |
| VITE_API_BASE_URL | - | 前端生产构建连接的后端 API 根路径；留空时使用静态 Mock 演示 |
| DATA_DIR | backend/data | 数据目录 |
| OUTPUT_DIR | backend/data/outputs | 输出目录 |

## 切换到真实模型

1. 设置 `.env` 中 `MOCK_MODE=false`
2. 设置 `OPENAI_COMPATIBLE_MODE=true`
3. 配置 `LLM_API_KEY` 和 `LLM_BASE_URL`
4. 重启后端服务

## 可选依赖

- `python-docx`：支持 .docx 文件解析
- `pypdf`：支持 .pdf 文件解析

```bash
pip install python-docx pypdf
```
