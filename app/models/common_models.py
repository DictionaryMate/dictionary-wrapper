from datetime import datetime

from pydantic import BaseModel

from app.models.anki_models import AnkiAddNoteDto, AnkiAudio, AnkiField, AnkiNote


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

    def _to_anki_audio(self) -> AnkiAudio:
        file_name = f"{self.word}_{datetime.now().strftime('%s')}.mp3"
        return AnkiAudio(url=self.audioLink, filename=file_name, fields=["phonetic"])

    def _syn_or_ant_to_str(
        self, syn_or_ants: list[SynonymOrAntonym], top: int = 5
    ) -> str:
        return "<br>".join(
            [
                f"{syn_or_ant.partOfSpeech}: {self.__get_top_syn_or_ant(syn_or_ant, top)}"
                for syn_or_ant in syn_or_ants
                if len(syn_or_ant.words) > 0
            ]
        )

    def __get_top_syn_or_ant(self, syn_or_ant: SynonymOrAntonym, top: int) -> list[str]:
        return (
            syn_or_ant.words[:top] if len(syn_or_ant.words) > top else syn_or_ant.words
        )

    def to_anki_field(self):
        def_dicts = [d.model_dump() for d in self.definitions]
        def_strs = ["<br>".join(d.values()) for d in def_dicts]
        def_str = "<br><br>".join(def_strs)
        syn_str = self._syn_or_ant_to_str(self.synonyms)
        ant_str = self._syn_or_ant_to_str(self.antonyms)
        how_to_str = "<br>".join(self.howToUse)

        if (self.PIEroot is not None) and (len(self.PIEroot.sameRootWords) > 0):
            pie_root_str = (
                self.PIEroot.root + "<br>" + "<br>".join(self.PIEroot.sameRootWords)
            )
        else:
            pie_root_str = ""

        test_sentences = "<br>".join(
            [sentence.replace(self.word, "_______") for sentence in self.testSentences]
        )
        etymologies = "<br>".join(self.etymologies)

        return AnkiField(
            word=self.word,
            phonetic=self.phonetic,
            definitions=def_str,
            synonyms=syn_str,
            antonyms=ant_str,
            etymology=etymologies,
            PIEroot=pie_root_str,
            howToUse=how_to_str,
            testSentence=test_sentences,
            picture="",
        )

    def to_add_note_dto(self):
        if self.audioLink:
            note = AnkiNote(fields=self.to_anki_field(), audio=[self._to_anki_audio()])
        else:
            note = AnkiNote(fields=self.to_anki_field())
        dto = AnkiAddNoteDto(params={"note": note})

        return dto
