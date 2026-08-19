from fastapi import HTTPException, status
from backend.clients.translate import Translate
from backend.repositories.translate import TranslateRepository

translate_google = Translate()


class TranslateService:
    def __init__(self, repository: TranslateRepository):
        self.repository = repository

    async def translate_word(self, word: str):
        if not word or not word.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Word not found",
            )
        translated_word = await translate_google.translate(word=word.strip())
        result = await self.repository.create_translate(**translated_word.model_dump())
        return result 
