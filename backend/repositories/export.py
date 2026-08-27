from typing import Sequence
from backend.models.history import TranslationHistory
from sqlalchemy import select, RowMapping

class ExportRepository:
    def __init__(self, db):
        self.db = db

    async def get_translated_histories(self) -> Sequence[RowMapping]:
        model = [
            TranslationHistory.word,
            TranslationHistory.translation,
            TranslationHistory.transcription,
            TranslationHistory.score,
        ]
        request = await self.db.execute(select(*model).order_by(TranslationHistory.id))
        history = request.mappings().all()
        return history

    async def get_histories_by_range(self, start: int, end: int) -> Sequence[RowMapping]:
        offset = start - 1
        limit = end - start + 1
        model = [
            TranslationHistory.word,
            TranslationHistory.translation,
            TranslationHistory.transcription,
            TranslationHistory.score,
        ]
        request = await self.db.execute(select(*model).order_by(TranslationHistory.id)).offset(offset).limit(limit)
        history = request.mappings().all()
        return history
