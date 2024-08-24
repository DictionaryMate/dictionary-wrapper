import os

from dotenv import load_dotenv
from english_ipa.cambridge import CambridgeDictScraper  # type: ignore

from dictionary_wrapper import get_word_field
from dictionary_wrapper.clients.mw_client import MerriamWebsterClient
from dictionary_wrapper.clients.wordnik_client import WordnikClient
from dictionary_wrapper.models.syn_ant_enum import SynAntEnum

load_dotenv()

## get all the word fields
dictionary_api_key = os.getenv("MW_DICT_KEY")
thesaurus_api_key = os.getenv("MW_THE_KEY")
wordnik_api_key = os.getenv("WORDIK_API_KEY")

word = "gallant"

word_field = get_word_field(
    word,
    dictionary_api_key,  # type: ignore
    thesaurus_api_key,  # type: ignore
    wordnik_api_key,  # type: ignore
)

## get definitions from Merriam-Webster Dictionary
mw_client = MerriamWebsterClient(
    word,
    dictionary_api_key,  # type: ignore
    thesaurus_api_key,  # type: ignore
)
definition = mw_client.extract_definitions()

## get definitions, synonyms and antonyms from Merriam-Webster Thesaurus
synonyms = mw_client.extract_synonyms_or_antonyms(SynAntEnum.Synonym)
antonyms = mw_client.extract_synonyms_or_antonyms(SynAntEnum.Antonym)

## get audio link from Merriam-Webster Dictionary
audio_link = mw_client.extract_audio_link()

## get etymologies from Merriam-Webster Thesaurus
etymologies = mw_client.extract_etymologies()

## get example sentences from Wordnik
wordnik_client = WordnikClient(
    word,
    wordnik_api_key,  # type: ignore
)
example_sentences = wordnik_client.extract_example_sentences()

## get audio link from Wordnik
audio_link = wordnik_client.extract_audio_link()

## get ipa from Cambridge Dictionary
scraper = CambridgeDictScraper()
ipa = scraper.get_ipa_in_str(word)
