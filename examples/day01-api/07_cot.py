"""
Chain of Thought：让 AI 一步步思考
"""
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DP_API_KEY"),
    base_url=os.getenv("DP_URL")
)

# 不用 CoT
bad_response = client.chat.completions.create(
    model=os.getenv("DP_MODE"),
    messages=[
        {"role": "user", "content": "一个农场有15只鸡和12只鸭，卖掉了8只鸡和3只鸭，又买了5只鸭。现在农场一共有多少只家禽？直接给数字答案。"}
    ]
)
print("不用 CoT:", bad_response.choices[0].message.content)

# 用 CoT
good_response = client.chat.completions.create(
    model=os.getenv("DP_MODE"),
    messages=[
        {"role": "user", "content": """一个农场有15只鸡和12只鸭，卖掉了8只鸡和3只鸭，又买了5只鸭。
            现在农场一共有多少只家禽？

            请一步步思考：
            1. 先算鸡的数量变化
            2. 再算鸭的数量变化
            3. 最后算总数"""}
    ]
)
print("用 CoT:", good_response.choices[0].message.content)
