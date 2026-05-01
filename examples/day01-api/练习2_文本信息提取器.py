"""
练习 2：文本信息提取器
Few-shot + JSON 输出，提取结构化信息
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

# Few-shot 示例
few_shot = [
    {"input": "我叫李四，32岁，在北京字节跳动工作，职位是算法工程师，月薪40k",
     "output": {"name": "李四", "age": 32, "city": "北京", "company": "字节跳动", "position": "算法工程师", "salary": "40k"}},
    {"input": "我叫王小明，25岁，在上海腾讯工作，职位是前端开发，月薪20k",
     "output": {"name": "王小明", "age": 25, "city": "上海", "company": "腾讯", "position": "前端开发", "salary": "20k"}},
    {"input": "我叫赵丽，29岁，在深圳华为工作，职位是产品经理，月薪35k",
     "output": {"name": "赵丽", "age": 29, "city": "深圳", "company": "华为", "position": "产品经理", "salary": "35k"}},
]

messages = [
    {"role": "system", "content": "你是一个信息提取助手，从用户输入中提取结构化信息，以JSON格式输出。"}
]

for i in few_shot:
    messages.append({"role": "user", "content": i["input"]})
    messages.append({"role": "assistant", "content": json.dumps(i["output"], ensure_ascii=False)})

messages.append({"role": "user", "content": "我是张三，现在在成都，失业快一年了，之前在美团做数据分析,每个月到手130k。"})

response = client.chat.completions.create(
    model=os.getenv("DP_MODE"),
    messages=messages,
    temperature=0.01
)

print(response.choices[0].message.content)
