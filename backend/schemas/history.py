from pydantic import BaseModel, ConfigDict

class HistoryResponse(BaseModel):
    id: int
    word: str
    translation: str
    transcription: str | None = None
    score: int

    model_config = ConfigDict(from_attributes=True)

class HistoryListResponse(BaseModel):
    limit: int
    offset: int
    items: list[HistoryResponse]
