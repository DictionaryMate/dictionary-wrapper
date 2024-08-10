import sys
from pathlib import Path
from typing import Annotated

from app.clients._wm_utils import (
    extract_audio_link,
    extract_definitions,
    extract_etymologies,
    extract_synonyms_or_antonyms,
    form_url,
)
from app.exceptions import MerriamWebsterClientException

sys.path.append(str(Path(__file__).parent.parent))

import json

import requests

from app.config import MWDictType
from app.models.common_models import Definition, SynonymOrAntonym


class MerriamWebsterClient:
    def __init__(self, word: str) -> None:
        self.word = word
        self.dictionary_result = self._get_api_result(MWDictType.DICTIONARY)
        self.thesaurus_result = self._get_api_result(MWDictType.THESAURUS)

    def extract_audio_link(self) -> str | None:
        return extract_audio_link(self.dictionary_result)

    def extract_etymologies(self) -> list[str]:
        return extract_etymologies(self.word, self.dictionary_result)

    def extract_definitions(self) -> list[Definition]:
        return extract_definitions(self.word, self.dictionary_result)

    def extract_synonyms_or_antonyms(
        self, type: Annotated[str, "syns or ants"]
    ) -> list[SynonymOrAntonym]:
        return extract_synonyms_or_antonyms(self.word, self.thesaurus_result, type)

    def _get_api_result(self, dict_type: MWDictType) -> list[dict]:
        url = form_url(self.word, dict_type)
        try:
            req = requests.get(url)
        except requests.exceptions.SSLError:
            raise MerriamWebsterClientException(
                status_code=0, content="SSLError", url=url
            )
        if req.status_code != 200:
            raise MerriamWebsterClientException(
                status_code=req.status_code, content=req.content, url=url
            )

        return json.loads(req.content.decode())
