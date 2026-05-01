from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv("../.env")

client = OpenAI(
    api_key=os.getenv("DP_API_KEY"),
    base_url=os.getenv("DP_URL")
)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(req:ChatRequest):
    def generate():
        response  = client.chat.completions.create(
            model=os.getenv("DP_MODE"),
            messages=[
                {"role":"user","content":req.message}
            ],
            stream=True
        )

        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield content
    return StreamingResponse(generate(),media_type="text/plain")