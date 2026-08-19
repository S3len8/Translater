from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.history import TranslationHistory
from sqlalchemy import select

class HistoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_one(self, word_id: int) -> Optional[TranslationHistory]:
        query = select(TranslationHistory).where(TranslationHistory.id == word_id)
        result = await self.db.execute(query)
        return result.scalars().one_or_none()

    async def get_all(self, offset: int, limit: int) -> list:
        query = select(TranslationHistory).offset(offset).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
