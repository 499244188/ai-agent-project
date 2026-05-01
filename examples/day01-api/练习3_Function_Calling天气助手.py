"""
练习 3：Function Calling 天气助手
多轮对话 + 工具调用 + 流式输出
"""
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DP_API_KEY"),
    base_url=os.getenv("DP_URL")
)

def get_weather(city: str) -> str:
    """模拟天气查询"""
    mock_data = {
        "北京": {"temperature": 28, "weather": "晴", "humidity": 45, "wind": "北风3级"},
        "上海": {"temperature": 31, "weather": "多云", "humidity": 72, "wind": "东南风2级"},
        "杭州": {"temperature": 29, "weather": "小雨", "humidity": 80, "wind": "东风2级"},
        "成都": {"temperature": 26, "weather": "阴", "humidity": 65, "wind": "微风"},
        "深圳": {"temperature": 33, "weather": "雷阵雨", "humidity": 85, "wind": "南风3级"},
    }
    data = mock_data.get(city)
    if data:
        return json.dumps(data, ensure_ascii=False)
    return json.dumps({"error": f"未找到 {city} 的天气数据"}, ensure_ascii=False)

def calculate(expression: str) -> str:
    """计算器"""
    try:
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return json.dumps({"error": "表达式包含非法字符"}, ensure_ascii=False)
        result = eval(expression)
        return json.dumps({"expression": expression, "result": result}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"计算出错: {str(e)}"}, ensure_ascii=False)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "可以查询指定城市的天气，温度，湿度，风力等信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称，如北京，上海，杭州"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "可以计算数学表达式，仅仅支持加减乘除跟括号",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式，例如：(2+3)*4"}
                },
                "required": ["expression"]
            }
        }
    },
]

available_functions = {"get_weather": get_weather, "calculate": calculate}

messages = [
    {"role": "system", "content": "你是一个智能助手，可以查询天气和进行数学计算，请用中文回答。"}
]

print("=" * 50)
print("  天气 & 计算器助手（输入 quit 退出）")
print("=" * 50)

while True:
    user_input = input("\n你=>: ")
    if user_input.lower() == "quit":
        print("再见！")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=os.getenv("DP_MODE"),
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    assistant_message = response.choices[0].message
    messages.append(assistant_message)

    if assistant_message.tool_calls:
        for tool_call in assistant_message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)

            print(f"\n [调用工具] {func_name}({func_args})")
            func_result = available_functions[func_name](**func_args)
            print(f" [工具返回] {func_result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": func_result
            })

        second_response = client.chat.completions.create(
            model=os.getenv("DP_MODE"),
            messages=messages,
        )
        final = second_response.choices[0].message
        messages.append(final)
        print(f"\n AI: {final.content}")
    else:
        print(f"\n AI: {assistant_message.content}")
