from pydantic import BaseModel

class TranslateResponse(BaseModel):
    message: str
    translation_id: int

class TranslateRequest(BaseModel):
    word: str

class TranslationResult(BaseModel):
    word: str
    translation: str
    transcription: str | None = None
    