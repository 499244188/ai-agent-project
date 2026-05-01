"""
Day 3 - Agent v1：单次工具调用
最基础的 Function Calling：LLM 决定调用什么工具 → 你执行 → 结果喂回去
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

# ========== 第一步：定义工具 ==========
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
                        "description": "数学表达式，如 123+23*23"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# ========== 第二步：工具的 Python 实现 ==========
def calculate(expression):
    try:
        result = eval(expression)
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        return f"计算出错: {e}"

tool_map = {"calculate": calculate}

# ========== 第三步：发请求 ==========
question = "帮我算一下 1234 * 5678 + 9999"

response = client.chat.completions.create(
    model=os.getenv("DP_MODE"),
    messages=[{"role": "user", "content": question}],
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message

# ========== 第四步：看 LLM 的决定 ==========
if message.tool_calls:
    tool_call = message.tool_calls[0]
    func_name = tool_call.function.name
    func_args = json.loads(tool_call.function.arguments)

    print(f"LLM 决定调用: {func_name}({func_args})")

    result = tool_map[func_name](**func_args)
    print(f"工具返回: {result}")

    # 结果喂回 LLM
    messages = [
        {"role": "user", "content": question},
        message,
        {"role": "tool", "tool_call_id": tool_call.id, "content": result}
    ]

    final_response = client.chat.completions.create(
        model=os.getenv("DP_MODE"),
        messages=messages
    )
    print(f"最终回答: {final_response.choices[0].message.content}")
else:
    print(f"LLM 直接回答: {message.content}")
