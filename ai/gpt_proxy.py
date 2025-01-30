
from openai import AsyncOpenAI
from data_project import TOKEN_AI, URL_AI
import asyncio


client = AsyncOpenAI(
    api_key=TOKEN_AI,
    base_url= URL_AI
)


async def gpt_response(content):
    try:
        response = await client.chat.completions.create(
            messages= [{"role": "user", "content": content}],
            model="gpt-4o-mini",
            max_tokens=1024,
            stream=False
        )
        print(1)
        return response.choices[0].message.content
    except Exception as e:
        print(e)


