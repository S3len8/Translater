from pydantic import BaseModel, ConfigDict


class TranslateRequest(BaseModel):
    word: str

class TranslateResponse(BaseModel):
    word: str
    translation: str
    transcription: str | None = None

    model_config = ConfigDict(from_attributes=True)