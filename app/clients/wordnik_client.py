import bs4 as bs
import requests

import app.config as config
from app.exceptions import WordnikClientException
from app.models.wordnik_models import WordnikAudio


class WordnikClient:
    def __init__(self, word: str) -> None:
        self.word = word

    def extract_audio_link(self) -> str | None:
        url = f"{config.WORDNIK_API_BASE_URL}/{self.word}/audio?useCanonical=false&limit=50&api_key={config.WORDNIK_API_KEY}"
        response = requests.get(url)
        if response.status_code != 200:
            raise WordnikClientException(
                status_code=response.status_code, content=response.content, url=url
            )

        if response.status_code == 404:
            return None

        response_list = response.json()
        wordnik_audios = [WordnikAudio(**d) for d in response_list]

        macmillan = [w for w in wordnik_audios if w.createdBy == "macmillan"]

        return macmillan[0].fileUrl if len(macmillan) > 0 else wordnik_audios[0].fileUrl

    def extract_etymologies(self) -> list[str]:
        url = f"{config.WORDNIK_API_BASE_URL}/{self.word}/etymologies?useCanonical=false&api_key={config.WORDNIK_API_KEY}"
        response = requests.get(url)
        if response.status_code != 200:
            raise WordnikClientException(
                status_code=response.status_code, content=response.content, url=url
            )

        if response.status_code == 404:
            return None

        ety_list = response.json()

        return [WordnikClient._parse_xml(ety) for ety in ety_list]

    def extract_example_sentences(self) -> list[str]:
        url = f"{config.WORDNIK_API_BASE_URL}/{self.word}/examples?includeDuplicates=false&useCanonical=false&limit=10&api_key={config.WORDNIK_API_KEY}"
        response = requests.get(url)
        if response.status_code != 200:
            raise WordnikClientException(
                status_code=response.status_code, content=response.content, url=url
            )

        if response.status_code == 404:
            return []

        sentence_objs = response.json().get("examples", [])

        sentences = [sentence_obj.get("text", "") for sentence_obj in sentence_objs]
        return list(filter(lambda x: len(x) > 0, sentences))

    @staticmethod
    def _parse_xml(content: str) -> str:
        return bs.BeautifulSoup(content, "xml").text
