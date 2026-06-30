from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class Club(Base):
    __tablename__ = "clubs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    country: Mapped[str] = mapped_column(
        String(100)
    )

    founded: Mapped[int] = mapped_column(
        Integer
    )

    stadium: Mapped[str] = mapped_column(
        String(100)
    )

    trophies: Mapped[int] = mapped_column(
        Integer,
        default=0
    )
