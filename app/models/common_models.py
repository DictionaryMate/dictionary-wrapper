from pydantic import BaseModel


class Definition(BaseModel):
    partOfSpeech: str
    detail: str
    exampleSentence: str


class SynonymOrAntonym(BaseModel):
    partOfSpeech: str
    detail: str
    words: list[str]


class _PIEroot(BaseModel):
    root: str
    sameRootWords: list[str]


class WordField(BaseModel):
    word: str
    phonetic: str
    definitions: list[Definition]
    synonyms: list[SynonymOrAntonym]
    antonyms: list[SynonymOrAntonym]
    etymologies: list[str]
    PIEroot: _PIEroot | None = None
    howToUse: list[str] = []
    testSentences: list[str]
    audioLink: str | None = None
    audioLink: str | None = None
