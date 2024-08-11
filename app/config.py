"""Configurations."""

import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

# merriam webster config
MW_BASE_URL = "https://dictionaryapi.com/api/v3/references"


class MWDictType(Enum):
    DICTIONARY = "collegiate"
    THESAURUS = "thesaurus"


MW_API_CONFIG = {
    MWDictType.DICTIONARY.value: {
        "key": os.getenv("MW_DICT_KEY"),
        "url": f"{MW_BASE_URL}/{MWDictType.DICTIONARY.value}/json",
    },
    MWDictType.THESAURUS.value: {
        "key": os.getenv("MW_THE_KEY"),
        "url": f"{MW_BASE_URL}/{MWDictType.THESAURUS.value}/json",
    },
}

MW_AUDIO_BASE_URL = "https://media.merriam-webster.com/audio/prons/en/us"
MW_AUDIO_FORMAT = "mp3"

# wordnik config
WORDNIK_API_KEY = os.getenv("WORDIK_API_KEY")
WORDNIK_API_BASE_URL = "https://api.wordnik.com/v4/word.json"
