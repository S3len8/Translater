from fastapi import HTTPException, status
from repositories.history import HistoryRepository
from clients.translate import Translate

translate_google = Translate()


class TranslateService:
    def __init__(self, history_repo: HistoryRepository):
        self.history_repo = history_repo

    async def is_translated(self, word: str, translation: str, transcription: str | None = None):
        if not word or not word.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Word not found",
            )
        if not translation or not translation.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Word not found",
            )

        print(word, translation, transcription)
        word_database = await self.history_repo.create_history(
            word=word.strip(),
            translation=translation.strip(),
            transcription=transcription)
        print(word_database)
        return word_database

    async def translate_word(self, word: str):
        if not word or not word.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Word not found",
            )
        result = await translate_google.translate()
        return result 