from fastapi import FastAPI,HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
# from openai import OpenAI
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import json
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    # 必填，没有就报错
    dp_api_key:str  
    # 有默认值
    dp_url:str = "https://api.deepseek.com"
    #有默认值
    dp_mode:str = "deepseek-v4-flash"
    # 可选
    al_em_key:str=""
    # 默认值
    al_em_mode:str="text-embedding-v4"
    # 默认值
    al_em_url:str="https://dashscope.aliyuncs.com/compatible-mode/v1"

    model_config = ConfigDict(env_file="../.env")

# 启动时自动读 .env，缺必填项直接报错
settings = Settings()
print(f"配置加载成功！模型：{settings.dp_mode}，URL：{settings.dp_url}")

load_dotenv("../.env")

client = AsyncOpenAI(
    api_key=os.getenv("DP_API_KEY"),
    base_url=os.getenv("DP_URL")
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(req:ChatRequest):
    try:
        async def generate():
            response  = await client.chat.completions.create(
                model=os.getenv("DP_MODE"),
                messages=[
                    {"role":"user","content":req.message}
                ],
                stream=True
            )

            async for chunk in response:
                content = chunk.choices[0].delta.content
                if content is not None:
                    yield content
        return StreamingResponse(generate(),media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"出错了：{str(e)}")