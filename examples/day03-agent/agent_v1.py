
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

    }
]

def calculate(expression):
    """LLM 说要调用calculate，python就执行这个函数"""
    try:
        result = eval(expression)
        return f"计算结果：{expression}={result}"
    except Exception as e:
        return f"计算出错了{e}"


tool_map={"calculate":calculate}

question = "请帮我算一下10个人分100个橘子，每个人的数量需要不同，那么拿的最多的人，最少可以拿几个？"
question = "帮我算一下 1234 * 5678 + 9999"
response = client.chat.completions.create(
    model=os.getenv("DP_MODE"),
    messages=[
        {"role":"user","content":question}
    ],
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message

if message.tool_calls:
    tool_call = message.tool_calls[0]
    func_name = tool_call.function.name
    func_args = json.loads(tool_call.function.arguments)

    print(f"LLM 决定调用:{func_name}({func_args})")

    result=tool_map[func_name](**func_args)
    print(f"工具返回:{result}")

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
    print(f"LLM 直接回答：{message.content}")
