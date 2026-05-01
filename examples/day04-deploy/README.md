# Day 4：Agent 部署 — 从脚本到服务

## 为什么要学部署？

你前三天写的代码，都是在终端里运行的。只有你自己能用。
部署就是把你的 Agent 变成一个"服务"，别人可以通过网络调用它。

面试时面试官会问：
- "你的 Agent 怎么部署的？" → FastAPI + Docker
- "支持流式输出吗？" → SSE/StreamingResponse
- "能同时处理多个请求吗？" → async 异步
- "配置怎么管理的？" → pydantic-settings

---

## 教学大纲

### 第一部分：FastAPI 接口层

#### 1.1 最小 API（已完成 ✅）
- 文件：`01_hello.py`
- 知识点：FastAPI、路由、GET 请求

#### 1.2 POST 请求和请求体（已完成 ✅）
- 文件：`02_post.py` → `04_body.py`
- 知识点：POST、Pydantic BaseModel、JSON 请求体

#### 1.3 调用 LLM 的 API（已完成 ✅）
- 文件：`03_llm.py` → `05_agent_api.py`
- 知识点：把 Agent 逻辑包进接口

#### 1.4 流式输出（已完成 ✅）
- 文件：`06_streaming.py`
- 知识点：StreamingResponse、yield、stream=True

#### 1.5 async 异步（待学）
- 文件：`07_async.py`
- 知识点：async/await、为什么 Agent 接口必须用异步
- 重要性：⭐⭐⭐ 面试必问

**为什么需要 async？**

同步版本：
```python
@app.post("/chat")
def chat(req: ChatRequest):  # 同步函数
    # 调 LLM 要等 3 秒
    # 这 3 秒内，其他用户的请求全部排队等着
    response = client.chat.completions.create(...)
    return response
```

异步版本：
```python
@app.post("/chat")
async def chat(req: ChatRequest):  # 异步函数
    # 调 LLM 要等 3 秒
    # 等待期间，FastAPI 可以去处理其他用户的请求
    response = await async_client.chat.completions.create(...)
    return response
```

Agent 调 LLM 通常要 2-10 秒，如果用同步，10 个人同时问就要等 20-100 秒。
用异步，10 个人同时问，每个人还是只等 2-10 秒。

核心语法就两个关键词：
- `async def` — 声明这是一个异步函数
- `await` — "在这里等一下，但不阻塞其他任务"

注意：用 async 时，OpenAI 客户端要用 `AsyncOpenAI` 而不是 `OpenAI`：
```python
from openai import AsyncOpenAI
client = AsyncOpenAI(...)
response = await client.chat.completions.create(...)
```

#### 1.6 错误处理（待学）
- 文件：`08_error.py`
- 知识点：try/except、HTTPException、统一错误响应
- 重要性：⭐⭐⭐ 没有错误处理的 API 是半成品

**为什么需要？**

Agent 调 LLM 可能失败：网络超时、API Key 无效、余额不足……
没有错误处理的话，用户看到的是一堆看不懂的报错。

```python
from fastapi import HTTPException

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        response = await client.chat.completions.create(...)
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent 出错了: {str(e)}")
```

#### 1.7 CORS 跨域（待学）
- 文件：`09_cors.py`
- 知识点：什么是跨域、为什么前端调接口需要 CORS
- 重要性：⭐⭐ 只要前后端分离就必须用

**什么是 CORS？**

你的前端页面在 `http://localhost:3000`，后端 API 在 `http://localhost:8000`。
浏览器默认禁止"不同地址"之间的请求，这叫"跨域"。
CORS 就是告诉浏览器："我允许别人调我的接口"。

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 允许所有来源（开发时用）
    allow_methods=["*"],       # 允许所有方法
    allow_headers=["*"],       # 允许所有头
)
```

---

### 第二部分：配置管理

#### 2.1 环境变量回顾（已了解 ✅）
- `.env` 文件、`os.getenv()`

#### 2.2 pydantic-settings（待学）
- 文件：`10_config.py`
- 知识点：用 Pydantic 管理配置，类型验证、默认值
- 重要性：⭐⭐ 真实项目都这么用

**为什么不用 os.getenv？**

```python
# 丑陋的方式
api_key = os.getenv("DP_API_KEY")        # 可能是 None
base_url = os.getenv("DP_URL")           # 可能拼写错误
model = os.getenv("DP_MODE")             # 没有类型检查
```

```python
# pydantic-settings 的方式
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    dp_api_key: str
    dp_url: str = "https://api.deepseek.com"
    dp_mode: str = "deepseek-chat"
    al_em_key: str
    al_em_mode: str = "text-embedding-v2"

    class Config:
        env_file = "../.env"

settings = Settings()  # 自动从 .env 读取，类型不对会报错
```

---

### 第三部分：项目结构

#### 3.1 真实项目的目录组织（待学）
- 知识点：路由拆分、APIRouter
- 重要性：⭐⭐ 面试会问"你的项目结构怎么组织的"

**你现在的代码全部塞在一个文件里，真实项目会拆开：**

```
ai-agent-api/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI 应用入口
│   ├── config.py          # 配置管理
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── chat.py        # 聊天接口
│   │   └── health.py      # 健康检查接口
│   └── services/
│       ├── __init__.py
│       └── agent.py       # Agent 核心逻辑
├── .env
├── requirements.txt
├── Dockerfile
└── README.md
```

好处：
- `main.py` 很干净，只有应用初始化
- 路由按功能拆分，好找
- Agent 逻辑独立，可以单独测试

---

### 第四部分：Docker 容器化

#### 4.1 Dockerfile（已写 ✅）
- 基础镜像、COPY、RUN、CMD

#### 4.2 docker build 和 docker run（待实操）
- 知识点：构建镜像、运行容器、端口映射
- 重要性：⭐⭐⭐ 部署核心

```bash
# 构建镜像
docker build -t agent-api .

# 运行容器
docker run -p 8000:8000 \
  -e DP_API_KEY=你的key \
  -e DP_URL=https://api.deepseek.com \
  -e DP_MODE=deepseek-chat \
  agent-api
```

#### 4.3 docker-compose（待学）
- 知识点：多服务编排（API + 数据库 + 向量库）
- 重要性：⭐⭐ 真实项目通常有多个服务

```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DP_API_KEY=你的key
      - DP_URL=https://api.deepseek.com
```

#### 4.4 .dockerignore（待学）
- 知识点：排除不需要复制到镜像的文件
- 跟 .gitignore 类似

---

### 第五部分：部署上线（了解即可）

#### 5.1 云服务器
- 阿里云 / 腾讯云 ECS
- 把 Docker 镜像推到服务器上运行

#### 5.2 域名和 HTTPS
- 买域名 → 解析到服务器 → 配置 Nginx

这部分有服务器再实操，现在先了解概念。

---

## 今天已完成的练习

| 文件 | 内容 | 状态 |
|------|------|------|
| 01_hello.py | 最小 GET API | ✅ |
| 02_post.py | POST 请求 | ✅ |
| 03_llm.py | 调用 DeepSeek | ✅ |
| 04_body.py | JSON 请求体 | ✅ |
| 05_agent_api.py | Agent API | ✅ |
| 06_streaming.py | 流式输出 | ✅ |
| Dockerfile | 容器化配置 | ✅ |

## 接下来要学的（按顺序）

1. `07_async.py` — async 异步
2. `08_error.py` — 错误处理
3. `09_cors.py` — CORS 跨域
4. `10_config.py` — pydantic-settings 配置管理
5. 项目结构重构
6. Docker 实操

---

## 面试话术

> "我用 FastAPI 把 Agent 封装成 REST API，支持流式输出。
> 用 async 异步处理并发请求，用 Pydantic 做数据验证。
> 最后用 Docker 打包，一条命令就能部署到任何服务器。"

这句话涵盖了今天所有知识点。背下来。
