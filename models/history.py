from models.base import Base, IDMixin, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class TranslationHistory(Base, IDMixin, TimestampMixin):
    __tablename__ = "translation_history"

    word: Mapped[str] = mapped_column(String, nullable=False)
    translation: Mapped[str] = mapped_column(String, nullable=False)
    transcription: Mapped[str | None] = mapped_column(String, nullable=True) 