from sqlalchemy import create_engine, String, Integer, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

DATABASE_URL = "sqlite:///./footballverse.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    nationality: Mapped[str] = mapped_column(String(100), default="")
    date_of_birth: Mapped[str] = mapped_column(String(50), default="")
    position: Mapped[str] = mapped_column(String(100), default="")
    biography: Mapped[str] = mapped_column(Text, default="")
    career_summary: Mapped[str] = mapped_column(Text, default="")
    international_career: Mapped[str] = mapped_column(Text, default="")
    goals: Mapped[int] = mapped_column(Integer, default=0)
    appearances: Mapped[int] = mapped_column(Integer, default=0)
    assists: Mapped[int] = mapped_column(Integer, default=0)
    trophies: Mapped[int] = mapped_column(Integer, default=0)

Base.metadata.create_all(engine)

print("=== FOOTBALLVERSE DATABASE READY ===")
print("Database: footballverse.db")
print("Table: players")
