import asyncio

from app.run import get_word_field_async

word = "gallant"


async def main():
    word_field = await get_word_field_async(word)
    print(word_field)


asyncio.run(main())
