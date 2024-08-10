import asyncio
import time

import aiohttp

from app.clients._wm_utils import (
    extract_audio_link,
    extract_definitions,
    extract_etymologies,
    extract_synonyms_or_antonyms,
)
from app.clients.mw_client_async import AsyncMerriamWebsterClient
from app.clients.wordnit_client_async import AsyncWordnikClient
from app.config import MWDictType
from app.models.common_models import WordField

word = "gallant"
wordnik_client = AsyncWordnikClient(word)
mw_client = AsyncMerriamWebsterClient(word)


async def fetch():
    async with aiohttp.ClientSession() as session:
        mw_dictionary = asyncio.create_task(
            mw_client.get_api_result(session, MWDictType.DICTIONARY)
        )
        mw_thesaurus = asyncio.create_task(
            mw_client.get_api_result(session, MWDictType.THESAURUS)
        )
        sentences = asyncio.create_task(
            wordnik_client.extract_example_sentences(session)
        )

        return await asyncio.gather(mw_dictionary, mw_thesaurus, sentences)


async def main():
    mw_dict, mw_thesaurus, sentences = await fetch()
    definitions = extract_definitions(word, mw_dict)
    ipa_in_str = ""
    etymologies = extract_etymologies(word, mw_thesaurus)
    syns = extract_synonyms_or_antonyms(word, mw_thesaurus, "syns")
    ants = extract_synonyms_or_antonyms(word, mw_thesaurus, "ants")
    audio_link = extract_audio_link(mw_dict)

    word_object = WordField(
        word=word,
        phonetic=ipa_in_str,
        definitions=definitions,
        etymologies=etymologies,
        synonyms=syns,
        antonyms=ants,
        testSentences=sentences,
        audioLink=audio_link,
    )

    anki_dto = word_object.to_anki_field()
    print(anki_dto)
    print("\n")


start_time = time.time()
asyncio.run(main())
print(f"Async Done in {time.time() - start_time} seconds")
