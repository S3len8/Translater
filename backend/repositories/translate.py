from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.history import TranslationHistory

class TranslateRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_translate(self, word: str, translation: str, transcription: str | None = None) -> TranslationHistory:
        translate_entry = TranslationHistory(word=word, translation=translation, transcription=transcription)
        self.db.add(translate_entry)
        print("💾 Записуємо в БД...")
        await self.db.commit()
        print("✅ Успішно збережено в БД!")
        await self.db.refresh(translate_entry)
        return translate_entry