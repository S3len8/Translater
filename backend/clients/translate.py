import httpx
from backend.schemas.translate import TranslationResult


MYMEMORY_TRANSLATE_URL = "https://api.mymemory.translated.net/get"
MYMEMORY_LANG_PAIR = "en|uk"
MYMEMORY_MAX_QUERY_BYTES = 500


class TranslationProviderError(Exception):
    """Raised when the translation provider cannot return a translation."""


class TranslationInputTooLongError(ValueError):
    """Raised when the text exceeds MyMemory's query size limit."""


class Translate:
    async def translate(self, word: str) -> TranslationResult:
        if len(word.encode("utf-8")) > MYMEMORY_MAX_QUERY_BYTES:
            raise TranslationInputTooLongError(
                "The word exceeds MyMemory's 500-byte query limit"
            )

        params = {
            "q": word,
            "langpair": MYMEMORY_LANG_PAIR,
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    MYMEMORY_TRANSLATE_URL,
                    params=params,
                )
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPStatusError as error:
            raise TranslationProviderError(
                f"MyMemory returned HTTP {error.response.status_code}"
            ) from error
        except (httpx.RequestError, ValueError) as error:
            raise TranslationProviderError(
                "MyMemory request failed"
            ) from error

        translated_text = data.get("responseData", {}).get("translatedText")
        response_status = data.get("responseStatus")

        if response_status != 200:
            raise TranslationProviderError(
                f"MyMemory returned status {response_status}"
            )

        if not isinstance(translated_text, str) or not translated_text.strip():
            raise TranslationProviderError(
                "MyMemory returned an empty translation"
            )

        return TranslationResult(
            word=word,
            translation=translated_text,
            transcription=None,
        )
