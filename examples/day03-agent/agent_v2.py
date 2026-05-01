
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DP_API_KEY"),
    base_url=os.getenv("DP_URL")
)


tools = [
    {
        "type":"function",
        "function":{
            "name":"calculate",
            "description":"这个工具主要用来执行数学计算，传入表达式，返回结果",
            "parameters":{
                "type":"object",
                "properties":{
                    "expression":{
                        "type":"string",
                        "description":"数学表达式，如 123+23*23"
                    }
                },
                "required":["expression"]

            }

        }

    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "搜索互联网获取信息。当用户问实时信息时使用。",
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
    """LLM 说要调用calculate，python就执行这个函数"""
    try:
        result = eval(expression)
        return f"计算结果：{expression}={result}"
    except Exception as e:
        return f"计算出错了{e}"

def search_web(query):
    return f'关于"{query}" 的结果搜索：这是模拟内容，真实内容需要接入搜索API.'



tool_map={"calculate":calculate,"search_web":search_web}

# question = "请帮我算一下10个人分100个橘子，每个人的数量需要不同，那么拿的最多的人，最少可以拿几个？"
question = input("✅你：")

messages = [{"role":"user","content":question}]

for round_num in range(5):
    print(f"\n==========第 {round_num+1} 轮对话==========")

    response = client.chat.completions.create(
        model=os.getenv("DP_MODE"),
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if message.tool_calls:
        messages.append(message)

        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)

            print(f"调用工具：{func_name}({func_args})")
            result = tool_map[func_name](**func_args)
            print(f"工具返回：{result[:100]}$$$...")

            messages.append({
                "role":"tool",
                "tool_call_id":tool_call.id,
                "content":result
            })
    elif message.content:
        print(f"\n最终回答：{message.content}")
        break
