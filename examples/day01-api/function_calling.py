"""
Day 1 - Function Calling 基础
让 LLM 不只会聊天，还能"做事"——调用你定义的工具
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

# ========== 定义工具 ==========
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如：北京"
                    }
                },
                "required": ["city"]
            }
        }
    },
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

def get_weather(city):
    weather_data = {
        "北京": "晴天，23℃",
        "上海": "多云，22℃",
    }
    return weather_data.get(city, f"没有{city}的天气数据")

def calculate(expression):
    try:
        return str(eval(expression))
    except:
        return "计算错误"

# ========== 发请求 ==========
response = client.chat.completions.create(
    model=os.getenv("DP_MODE"),
    messages=[{"role": "user", "content": "北京今天天气怎么样？另外帮我算一下 123*456+789"}],
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message

# ========== 处理工具调用 ==========
if message.tool_calls:
    tool_messages = []
    for tool_call in message.tool_calls:
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)
        print(f"AI 想调用: {func_name}({func_args})")

        if func_name == "get_weather":
            result = get_weather(func_args["city"])
        elif func_name == "calculate":
            result = calculate(func_args["expression"])

        print(f"工具结果: {result}")

        tool_messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })

    # 结果喂回 LLM
    response2 = client.chat.completions.create(
        model=os.getenv("DP_MODE"),
        messages=[
            {"role": "user", "content": "北京今天天气怎么样？另外帮我算一下 123*456+789"},
            message,
            *tool_messages
        ]
    )
    print(f"\nAI 最终回复: {response2.choices[0].message.content}")
else:
    print("AI 没有调用工具，直接回复:", message.content)
