from fastapi import HTTPException, status
from backend.repositories.history import HistoryRepository

class HistoryService:
    def __init__(self, repository: HistoryRepository):
        self.repository = repository

    async def get_word(self, word_id: int):
        if word_id < 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        word = await self.repository.get_one(word_id=word_id)

        if word is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Translation not found",
            )
        
        return word

    async def get_all_words(self, offset: int, limit: int):
        if offset < 0 or limit < 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        words = await self.repository.get_all(offset=offset, limit=limit)
        return words