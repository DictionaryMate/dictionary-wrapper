"""Configurations."""

import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

# open ai config
OPEN_AI_API_KEY = os.getenv("OPEN_AI_KEY")
OPEN_AI_API_BASE = "https://francecentral.api.cognitive.microsoft.com/"
OPEN_AI_API_TYPE = "azure"
OPEN_API_API_VERSION = "2023-07-01-preview"
OEPN_AI_MODEL = "gpt-4_0613"

# g4f config
G4F_TIMEOUT = 120

# anki config
ANKI_CONNECT_VERSION = 6
ANKI_ADDRESS = "http://localhost"
ANKI_PORT = 8765
ANKI_DECK_NAME = "EnglishVocabAI"
ANKI_MODEL_NAME = "EnglishVocabAI"

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

# redis config
REDIS_URL = os.getenv("REDIS_URL")


# celery config
class CeleryTaskName(Enum):
    CHECK_ANKI_HEALTH = "CHECK_ANKI_HEALTH"
    CHECK_ANKI_DUPLICATE = "CHECK_ANKI_DUPLICATE"
    GET_GPT_RESULT = "GET_GPT_RESULT"
    GET_AUDIO_LINK = "GET_AUDIO_LINK"
    CREATE_ANKI_NOTE = "CREATE_ANKI_NOTE"


# wordnik config
WORDNIK_API_KEY = os.getenv("WORDIK_API_KEY")
WORDNIK_API_BASE_URL = "https://api.wordnik.com/v4/word.json"

# base dir
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPT_DIR = os.path.join(BASE_DIR, "core", "gpt_prompt")
