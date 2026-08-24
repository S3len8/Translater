from fastapi import APIRouter, Depends, status
from backend.core.postgre import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from backend.repositories.translate import TranslateRepository
from backend.services.translate import TranslateService
from backend.schemas.translate import TranslateRequest, TranslateResponse

router = APIRouter()

def translate_service(db: AsyncSession = Depends(get_db)) -> TranslateService:
    repository = TranslateRepository(db)
    return TranslateService(repository)

@router.post("/translate", response_model=TranslateResponse, status_code=status.HTTP_201_CREATED)
async def translate(
        payload: TranslateRequest,
        service: TranslateService = Depends(translate_service)
):
    result = await service.translate_word(word=payload.word)
    return {
        "message": "Translation saved successfully",
        "translation_id": result.id,
        "word": result.word,
        "translation": result.translation,
        "transcription": result.transcription,
        "score": result.score 
    }
