import asyncio
import time

import aiohttp

from app.clients.wordnit_client_async import AsyncWordnikClient

client = AsyncWordnikClient("gallant")


async def main():
    async with aiohttp.ClientSession() as session:
        audio_link = asyncio.create_task(client.extract_audio_link(session))
        sentences = asyncio.create_task(client.extract_example_sentences(session))

        await asyncio.gather(audio_link, sentences)


start_time = time.time()
asyncio.run(main())
print(f"Async Done in {time.time() - start_time} seconds")
