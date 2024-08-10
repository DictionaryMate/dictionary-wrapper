from english_ipa.cambridge import CambridgeDictScraper

from app.clients.mw_client import MerriamWebsterClient
from app.clients.wordnik_client import WordnikClient
from app.models.common_models import WordField

word = "gallant"

mw_client = MerriamWebsterClient(word)
definitions = mw_client.extract_definitions()
etymologies = mw_client.extract_etymologies()
syns = mw_client.extract_synonyms_or_antonyms("syns")
ants = mw_client.extract_synonyms_or_antonyms("ants")
audio_link = mw_client.extract_audio_link()

wordnik_client = WordnikClient(word)
sentences = wordnik_client.extract_example_sentences()

scraper = CambridgeDictScraper()
ipa_in_str = scraper.get_ipa_in_str(word)

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

# print(word_object)

anki_dto = word_object.to_anki_field()
print(anki_dto)
