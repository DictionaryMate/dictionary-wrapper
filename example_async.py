import asyncio
import os

from dotenv import load_dotenv

from dictionary_wrapper import get_word_field_async

load_dotenv()
dictionary_api_key = os.getenv("MW_DICT_KEY")
thesaurus_api_key = os.getenv("MW_THE_KEY")
wordnik_api_key = os.getenv("WORDIK_API_KEY")

word = "gallant"


async def main():
    word_field = await get_word_field_async(
        word, dictionary_api_key, thesaurus_api_key, wordnik_api_key
    )
    print(word_field)


asyncio.run(main())
