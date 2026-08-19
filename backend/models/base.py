from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func


class Base(DeclarativeBase):
    pass

class IDMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now()) 