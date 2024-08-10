from enum import Enum

from pydantic import BaseModel, Field

import app.config as config


class AnkiAction(Enum):
    ADD_NOTE = "addNote"
    FIND_NOTES = "findNotes"
    GET_DECK_NAMES = "deckNames"
    CREATE_DECK = "createDeck"
    GET_MODEL_NAMES = "modelNames"


class AnkiAudio(BaseModel):
    url: str
    filename: str
    fields: list[str]


class _AnkiDeckDuplicateScopeOption(BaseModel):
    deckName: str = Field(default=config.ANKI_DECK_NAME)
    checkChildren: bool = Field(default=False)
    checkAllModels: bool = Field(default=False)


class AnkiDeckOption(BaseModel):
    allowDuplicate: bool = Field(default=False)
    duplicateScope: str = Field(default="deck")
    duplicateScopeOptions: _AnkiDeckDuplicateScopeOption = Field(
        default=_AnkiDeckDuplicateScopeOption()
    )


class AnkiField(BaseModel):
    word: str
    phonetic: str
    definitions: str
    synonyms: str
    antonyms: str
    etymology: str
    PIEroot: str
    howToUse: str
    testSentence: str
    picture: str | None = ""


class AnkiNote(BaseModel):
    fields: AnkiField
    deckName: str = Field(default=config.ANKI_DECK_NAME)
    modelName: str = Field(default=config.ANKI_MODEL_NAME)
    options: AnkiDeckOption = Field(default=AnkiDeckOption())
    tags: list[str] | None = None
    audio: list[AnkiAudio] | None = None
    video: list[dict] | None = None
    picture: list[dict] | None = None


class AnkiAddNoteDto(BaseModel):
    params: dict
    action: AnkiAction = Field(default=AnkiAction.ADD_NOTE)
    version: int = Field(default=config.ANKI_CONNECT_VERSION)
