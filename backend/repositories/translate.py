from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.history import TranslationHistory
from sqlalchemy import select, update

class TranslateRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_translate(self, word: str, translation: str, score: int, transcription: str | None = None) -> TranslationHistory:
        translate_entry = TranslationHistory(
            word=word,
            translation=translation,
            transcription=transcription,
            score=score,
        )

        self.db.add(translate_entry)
        print("💾 Записуємо в БД...")
        await self.db.commit()
        print("✅ Успішно збережено в БД!")
        await self.db.refresh(translate_entry)
        return translate_entry

    async def get_word(self, word: str) -> Optional[TranslationHistory]:
        query = await self.db.execute(
            select(TranslationHistory)
            .where(TranslationHistory.word == word)
        )
        return query.scalars().one_or_none()

    async def increment_count(self, word: str) -> TranslationHistory | None:
        query = (
            update(TranslationHistory)
            .where(TranslationHistory.word == word)
            .values(
                score=TranslationHistory.score + 1
            )
            .returning(TranslationHistory)
        )

        result = await self.db.execute(query)
        await self.db.commit()

        return result.scalar_one_or_none()
