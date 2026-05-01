from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv("../.env")

client = OpenAI(
    api_key=os.getenv("DP_API_KEY"),
    base_url=os.getenv("DP_URL")
)

app = FastAPI()

class AskRequest(BaseModel):
    question:str

@app.post("/ask")
def ask(req:AskRequest):
    response = client.chat.completions.create(
        model = os.getenv("DP_MODE"),
        messages=[
            {"role":"user","content":req.question}
        ]
    )
    answer = response.choices[0].message.content
    return {"answer":answer}