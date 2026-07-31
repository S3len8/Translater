from fastapi import APIRouter, Depends
from core.postgre import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.history import HistoryRepository
from services.translate import TranslateService
from schemas.translate import TranslateResponse, TranslateRequest

router = APIRouter()

def translate_service(db: AsyncSession = Depends(get_db)) -> TranslateService:
    repository = HistoryRepository(db)
    return TranslateService(repository)

@router.post("/translate", response_model=TranslateResponse)
async def get_translate(
        word: str,
        translation: str,
        transcription: str | None = None,
        service: TranslateService = Depends(translate_service)
):
    return await service.is_translated(word=word, translation=translation, transcription=transcription)