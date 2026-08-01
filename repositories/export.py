from typing import Sequence
from models.history import TranslationHistory
from sqlalchemy import select, RowMapping

class ExportRepository:
    def __init__(self, db):
        self.db = db

    async def get_translated_histories(self) -> Sequence[RowMapping]:
        model = [TranslationHistory.word, TranslationHistory.translation, TranslationHistory.transcription]
        request = await self.db.execute(select(*model).order_by(TranslationHistory.id))
        history = request.mappings().all()
        return history