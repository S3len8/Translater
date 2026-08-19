from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.postgre import get_db
from backend.repositories.history import HistoryRepository
from backend.services.history import HistoryService
from backend.schemas.history import HistoryResponse, HistoryListResponse

router = APIRouter()


def history_service(db: AsyncSession = Depends(get_db)) -> HistoryService:
    repository = HistoryRepository(db)
    return HistoryService(repository)

@router.get("/one_word", response_model=HistoryResponse)
async def one_word(
        word_id: int,
        service: HistoryService = Depends(history_service)
):
    return await service.get_word(word_id=word_id)

@router.get("/list_words", response_model=HistoryListResponse)
async def list_words(
        offset: int = 0,
        limit: int = 100,
        service: HistoryService = Depends(history_service)
):
    words = await service.get_all_words(offset=offset, limit=limit)

    return HistoryListResponse(
        limit=limit,
        offset=offset,
        items=words,
    )
