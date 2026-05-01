from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv("../.env")

client = OpenAI(
    api_key=os.getenv("DP_API_KEY"),
    base_url=os.getenv("DP_URL")
)

app = FastAPI()

@app.post("/ask")
def ask(question:str):
    response = client.chat.completions.create(
        model=os.getenv("DP_MODE"),
        messages=[
            {"role":"user","content":question}
        ],
    )

    answer = response.choices[0].message.content
    return {"answer":answer}