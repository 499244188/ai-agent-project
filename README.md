# AI Agent 学习项目

从零开始学习 AI Agent 开发：API 调用 → RAG 检索 → Agent 循环

纯 Python 实现，不依赖 LangChain 管道语法，每一步都能看懂。

## 技术栈

- **LLM**: DeepSeek（聊天）
- **Embedding**: 阿里 DashScope（向量化）
- **向量数据库**: ChromaDB
- **语言**: Python 3.11+

## 项目结构

```
ai-agent-project/
├── examples/
│   ├── day01-api/
│   │   └── function_calling.py    # Function Calling 基础
│   ├── day02-rag/
│   │   └── resume_qa.py           # RAG 简历问答助手
│   └── day03-agent/
│       ├── agent_v1_single_tool.py    # 单次工具调用
│       ├── agent_v2_loop.py           # Agent 循环（核心）
│       └── agent_v3_rag_tool.py       # RAG 变成 Agent 工具
├── data/
│   └── resumes/                   # 简历 PDF（需自行准备）
├── .env.example                   # 环境变量模板
└── .gitignore
```

## 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/你的用户名/ai-agent-project.git
cd ai-agent-project

# 2. 安装依赖
uv venv
uv pip install openai python-dotenv langchain langchain-community chromadb langchain-chroma dashscope pypdf

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 API Key

# 4. 运行
python examples/day03-agent/agent_v2_loop.py
```

## 学习路线

### Day 1：API 调用 + Function Calling

- 调用 DeepSeek API 发送第一句话
- Function Calling：让 LLM 能调用工具
- `tools` JSON 定义 → LLM 决策 → 执行 → 结果喂回

### Day 2：RAG 检索增强生成

- Embedding 文本向量化（阿里 DashScope API，不需要 PyTorch）
- ChromaDB 向量数据库
- PDF 加载 → 切分 → 向量化 → 检索 → LLM 回答

### Day 3：Agent 开发核心

- **v1**：单次工具调用（Function Calling 地基）
- **v2**：for 循环 + messages.append（Agent 核心秘密）
- **v3**：RAG 变成 Agent 的一个工具 + 对话记忆

## Agent 的核心原理

```
用户输入 → 放进 messages
  ↓
循环（最多 N 轮）：
  ↓
  发请求给 LLM
  ↓
  LLM 返回了什么？
  ├── tool_calls → 执行工具 → 结果放进 messages → 继续下一轮
  └── content → 打印 → break 退出
```

三个零件就够了：`tools` 定义、`tool_map` 实现、`for` 循环。

## API Key 申请

| 服务 | 用途 | 申请地址 |
|------|------|----------|
| DeepSeek | 聊天/推理 | https://platform.deepseek.com |
| 阿里 DashScope | Embedding 向量化 | https://dashscope.aliyun.com |

两个都有免费额度，入门阶段够用。
