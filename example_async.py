import asyncio
import os

import aiohttp
from dotenv import load_dotenv
from english_ipa.cambridge_async import AsyncCambridgeDictScraper

from dictionary_wrapper import get_word_field_async
from dictionary_wrapper.clients._wm_utils import (
    extract_definitions,
    extract_etymologies,
    extract_synonyms_or_antonyms,
)
from dictionary_wrapper.clients.mw_client_async import AsyncMerriamWebsterClient
from dictionary_wrapper.clients.wordnit_client_async import AsyncWordnikClient
from dictionary_wrapper.config import MWDictType
from dictionary_wrapper.models.common_models import WordField
from dictionary_wrapper.models.syn_ant_enum import SynAntEnum

load_dotenv()
dictionary_api_key = os.getenv("MW_DICT_KEY")
thesaurus_api_key = os.getenv("MW_THE_KEY")
wordnik_api_key = os.getenv("WORDIK_API_KEY")

word = "gallant"


## get all the word fields
async def main():
    word_field = await get_word_field_async(
        word, dictionary_api_key, thesaurus_api_key, wordnik_api_key
    )
    print(word_field)


asyncio.run(main())


## get api results from merriam-webster
async def fetch_mw_result(
    word: str, dictionary_api_key: str, thesaurus_api_key: str, wordnik_api_key: str
) -> WordField:
    mw_client = AsyncMerriamWebsterClient(word)
    async with aiohttp.ClientSession() as session:
        mw_dictionary = asyncio.create_task(
            mw_client.get_api_result(session, MWDictType.DICTIONARY, dictionary_api_key)
        )
        mw_thesaurus = asyncio.create_task(
            mw_client.get_api_result(session, MWDictType.THESAURUS, thesaurus_api_key)
        )

        return await asyncio.gather(mw_dictionary, mw_thesaurus)


## get definitions, synonyms and antonyms, etymology, audio link from Merriam-Webster Thesaurus
async def get_definitions(
    word: str, dictionary_api_key: str, thesaurus_api_key: str, wordnik_api_key: str
):
    dictionary_result, thesaurus_result = await fetch_mw_result(
        word, dictionary_api_key, thesaurus_api_key, wordnik_api_key
    )

    definitions = extract_definitions(word, dictionary_result)
    synonyms = extract_synonyms_or_antonyms(SynAntEnum.Synonym, thesaurus_result)
    antonyms = extract_synonyms_or_antonyms(SynAntEnum.Antonym, thesaurus_result)
    etymologies = extract_etymologies(word, dictionary_result)
    audio_link = extract_definitions(word, dictionary_result)

    return definitions, synonyms, antonyms, etymologies, audio_link


# get example sentences and audio link from Wordnik
async def fetch_wordnik_result(word: str, wordnik_api_key: str):
    wordnik_client = AsyncWordnikClient(word, wordnik_api_key)
    async with aiohttp.ClientSession() as session:
        example_sentences = asyncio.create_task(
            wordnik_client.extract_example_sentences(session)
        )

        audio_link = asyncio.create_task(wordnik_client.extract_audio_link(session))

        return await asyncio.gather(example_sentences, audio_link)


# get ipa from Cambridge Dictionary
async def get_ipa(word: str):
    scraper = AsyncCambridgeDictScraper()
    ipa = await scraper.get_ipa_in_str(word)

    return ipa
