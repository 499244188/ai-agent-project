"""
Day 3 - Agent v2：循环调用工具
加了 for 循环：LLM 可以多次调用工具，直到它觉得信息够了才回答
"""
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DP_API_KEY"),
    base_url=os.getenv("DP_URL")
)

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
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "搜索互联网获取信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    }
                },
                "required": ["query"]
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

def search_web(query):
    return f'关于"{query}"的搜索结果：这是模拟内容，真实项目需要接入搜索API。'

tool_map = {"calculate": calculate, "search_web": search_web}

# ========== Agent 循环（核心） ==========
question = input("你：")
messages = [{"role": "user", "content": question}]

for round_num in range(5):
    print(f"\n--- 第 {round_num + 1} 轮 ---")

    response = client.chat.completions.create(
        model=os.getenv("DP_MODE"),
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if message.tool_calls:
        messages.append(message)  # LLM 的决定加入历史

        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)

            print(f"  调用工具: {func_name}({func_args})")
            result = tool_map[func_name](**func_args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    elif message.content:
        print(f"\n最终回答: {message.content}")
        break
