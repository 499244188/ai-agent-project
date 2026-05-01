from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
# from openai import OpenAI
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv("../.env")

client = AsyncOpenAI(
    api_key=os.getenv("DP_API_KEY"),
    base_url=os.getenv("DP_URL")
)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(req:ChatRequest):
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