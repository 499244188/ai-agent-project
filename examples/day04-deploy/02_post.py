from fastapi import FastAPI

app = FastAPI()


@app.post("/ask")
def ask(question:str):
    answer = f"你问的是：{question}"
    return {"answer":answer}