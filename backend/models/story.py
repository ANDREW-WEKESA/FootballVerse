from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class Story(Base):
    __tablename__ = "stories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(200)
    )

    category: Mapped[str] = mapped_column(
        String(100)
    )

    description: Mapped[str] = mapped_column(
        Text
    )

    duration: Mapped[int] = mapped_column(
        Integer,
        default=60
    )
