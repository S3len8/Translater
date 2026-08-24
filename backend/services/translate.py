from fastapi import HTTPException, status
from backend.clients.translate import (
    Translate,
    TranslationInputTooLongError,
    TranslationProviderError,
)
from backend.repositories.translate import TranslateRepository

translate_mymemory = Translate()


class TranslateService:
    def __init__(self, repository: TranslateRepository):
        self.repository = repository

    async def translate_word(self, word: str):
        normalized_word = self._normalize(word=word)

        if not normalized_word:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Word not found",
            )

        get_word = await self.repository.get_word(word=normalized_word)

        if get_word is not None:
            updated_word = await self.repository.increment_count(word=normalized_word)
            return updated_word

        try:
            translated_word = await translate_mymemory.translate(
                word=normalized_word
            )
        except TranslationInputTooLongError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error
        except TranslationProviderError as error:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Translation provider unavailable",
            ) from error

        result = await self.repository.create_translate(
            word=normalized_word,
            translation=self._normalize(word=translated_word.translation),
            transcription=translated_word.transcription,
            score=1
        )
        return result

    @staticmethod
    def _normalize(word: str) -> str:
        normalized_word = word.strip().lower().capitalize()
        return normalized_word
