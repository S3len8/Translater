from sqlalchemy.ext.asyncio import AsyncSession
from models.history import TranslationHistory


class HistoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def create_history(self, word: str, translation: str, transcription: str | None = None) -> TranslationHistory:
        history_entry = TranslationHistory(word=word, translation=translation, transcription=transcription)
        self.db.add(history_entry)
        await self.db.commit()
        await self.db.refresh(history_entry)
        return history_entry