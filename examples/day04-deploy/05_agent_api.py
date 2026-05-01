from fastapi import FastAPI
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

# ========== 工具定义 ==========
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

def calculate(expression):
    try:
        result = eval(expression)
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        return f"计算出错: {e}"

tool_map = {"calculate": calculate}

# ========== 请求体 ==========
class ChatRequest(BaseModel):
    message: str

# ========== Agent 接口 ==========

@app.post("/chat")
def chat(req:ChatRequest):
    messages = [
        {"role":"user","content":req.message}
    ]

    # 最多循环5次
    for _ in range(5):
        response = client.chat.completions.create(
            model = os.getenv("DP_MODE"),
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        msg = response.choices[0].message

        if msg.tool_calls:
            messages.append(msg)
            for tc in msg.tool_calls:
                func_name = tc.function.name
                func_args = json.loads(tc.function.arguments)
                result = tool_map[func_name](**func_args)

                messages.append({
                    "role":"tool",
                    "tool_call_id":tc.id,
                    "content":result
                })
        else:
            return {"reply":msg.content}
    return {"reply":"达到最大轮数"}
