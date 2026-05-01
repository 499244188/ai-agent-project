from openai import AsyncOpenAI
from app.config import settings

client = AsyncOpenAI(
    api_key=settings.dp_api_key,
    base_url=settings.dp_url
)

async def chat_stream(message:str):
    response = await client.chat.completions.create(
        model=settings.dp_mode,
        messages=[
            {"role":"user","content":message}
        ],
        stream=True
    )

    async for chunk in response:
        content = chunk.choices[0].delta.content
        if content is not None:
            yield content