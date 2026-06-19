# BidPilot 昇腾 NPU 适配说明

## 概述

BidPilot 当前以 Mock 模式为主要演示方式，未来接入真实大语言模型时，可适配华为昇腾NPU进行本地推理部署。本文档说明适配方案。

## 适配架构

```
BidPilot 后端
    |
    +-- LLMClient（模型调用抽象层）
    |       |
    |       +-- Mock 模式（当前默认）
    |       +-- OpenAI Compatible 模式
    |       +-- 自定义模型模式 → 昇腾NPU部署
    |
    +-- BaseAgent（Agent抽象层）
            |
            +-- mock_run() → Mock模式
            +-- llm_run() → 真实模型调用
```

## 昇腾NPU部署方案

### 方案一：MindIE推理框架

1. 使用 MindIE（MindSpore Inference Engine）部署模型
2. MindIE 兼容 OpenAI API 格式
3. BidPilot 通过 `OPENAI_COMPATIBLE_MODE=true` 对接
4. 配置 `LLM_BASE_URL` 指向 MindIE 服务地址

### 方案二：CANN + ATLAS 推理

1. 使用华为 CANN（Compute Architecture for Neural Networks）推理框架
2. 将模型转换为 OM 格式
3. 使用 ATLAS 推理服务对外提供API
4. BidPilot 通过自定义模型模式对接

### 方案三：vLLM on Ascend

1. 使用 vLLM 的昇腾NPU版本
2. 兼容 OpenAI API 格式
3. 配置方式与方案一相同

## 适配步骤

### 1. 环境准备

```bash
# 安装 CANN 驱动和固件
# 安装 MindIE 或 vLLM-Ascend
# 确认 NPU 可用
npu-smi info
```

### 2. 模型部署

```bash
# 以 MindIE 为例
mindie-service --model-path /path/to/model --port 8001
```

### 3. BidPilot 配置

```env
MOCK_MODE=false
OPENAI_COMPATIBLE_MODE=true
LLM_API_KEY=your-key
LLM_BASE_URL=http://localhost:8001/v1
LLM_MODEL=model-name
```

### 4. 重启服务

```bash
uvicorn main:app --reload --port 8000
```

## 推荐模型

| 模型 | 参数量 | NPU显存需求 | 适用场景 |
|------|--------|------------|---------|
| GLM-4-9B | 9B | 1×Ascend 910B | Mock替代 |
| Qwen2-72B | 72B | 4×Ascend 910B | 高质量输出 |
| DeepSeek-V2-Lite | 16B | 2×Ascend 910B | 均衡方案 |

## 注意事项

1. 昇腾NPU适配为P2扩展方向，当前P0以Mock模式为主
2. 实际适配需要根据NPU型号和驱动版本调整
3. 模型推理效果取决于模型能力和提示工程
4. 生产部署需考虑并发、缓存和容错

## 当前状态

- [x] LLMClient 模型调用抽象层
- [x] OpenAI Compatible 接口支持
- [x] 自定义模型接口预留
- [ ] 昇腾NPU实际部署测试
- [ ] 模型提示工程优化
- [ ] 推理性能基准测试
