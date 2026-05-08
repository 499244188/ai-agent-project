
from openai import OpenAI
import json
from config import settings

from tools.search import search_documents
from tools.calculator import calculator
from tools.time_tool import get_current_time

#  DeepSeek 客户端
llm_client = OpenAI(
    api_key = settings.dp_api_key,
    base_url = settings.dp_url
)


# Agent 工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_documents",
            "description": "搜索知识库，查找相关信息",
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
    },
    {
        "type":"function",
        "function":{
            "name":"get_current_time",
            "description":"获取当前日期和时间",
            "parameters":{
                "type":"object",
                "properties":{}
            }
        }

    },
    {
        "type":"function",
        "function":{
            "name":"calculator",
            "description":"一个简单的计算器，可以进行数学计算",
            "parameters":{
                "type":"object",
                "properties":{
                    "par":{
                        "type":"string",
                        "description":"数学表达式，如 12+3*4"
                    }

                },
                "required":["par"]
            }
        }
    }
]

tool_funcionts = {
    "search_documents":search_documents,
    "get_current_time":get_current_time,
    "calculator":calculator,
}



def run_agent():
    while True:
        print("输入 quit 退出")
        userinput = input("用户：")
        if userinput.lower()=="quit":
            break

        messages = [
            {"role":"system","content":"你是一个知识库助手，用搜索工具查找信息来回答问题。"},
            {"role":"user","content":userinput}
        ]

        for _ in range(5):
            response = llm_client.chat.completions.create(
                model=settings.dp_mode,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )

            msg = response.choices[0].message

            if msg.tool_calls:
                # 有工具调用 → 执行工具把结果加入对话
                messages.append(msg)
                for tc in msg.tool_calls:

                    func = tool_funcionts[tc.function.name]
                    print(f"工具是：{func}")
                    args = json.loads(tc.function.arguments)
                    result = func(**args)
                    # if tc.function.name=="get_current_time":
                    #     print("调用：get_current_time")
                    #     result=get_current_time()
                    # elif tc.function.name=="search_documents":
                    #     print("调用：search_documents")
                    #     args = json.loads(tc.function.arguments)
                    #     results = search_documents(args["query"])
                    #     result = "\n".join(f"[{r[1]}]{r[0]}" for r in results)
                    # elif tc.function.name=="calculator":
                    #     print("调用：calculator")
                    #     args = json.loads(tc.function.arguments)
                    #     result = calculator(args["par"])
                    messages.append({
                        "role":"tool",
                        "tool_call_id":tc.id,
                        "content":result,
                    })
            else:
                # 没有工具调用 → 直接返回
                print(f"Agent:{msg.content}")
                break
