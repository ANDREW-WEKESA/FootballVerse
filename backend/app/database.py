from sqlalchemy import (
    create_engine, Integer, String, Text, Boolean, ForeignKey, JSON, DateTime
)
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship
from sqlalchemy.sql import func
from dotenv import load_dotenv
import os, sys, logging

load_dotenv()

logger = logging.getLogger(__name__)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable is not set.")
    sys.exit(1)

engine = create_engine(DATABASE_URL, poolclass=NullPool)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Club(Base):
    __tablename__ = "clubs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    country: Mapped[str] = mapped_column(String(100), default="")
    founded: Mapped[str] = mapped_column(String(50), default="")
    stadium: Mapped[str] = mapped_column(String(200), default="")
    trophies: Mapped[int] = mapped_column(Integer, default=0)


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    country: Mapped[str] = mapped_column(String(100), default="")
    position: Mapped[str] = mapped_column(String(100), default="")
    goals: Mapped[int] = mapped_column(Integer, default=0)
    trophies: Mapped[int] = mapped_column(Integer, default=0)
    external_id: Mapped[str] = mapped_column(String(200), default="")
    image_url: Mapped[str] = mapped_column(String(1000), default="")


class Story(Base):
    __tablename__ = "stories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(100), default="Football History")
    description: Mapped[str] = mapped_column(Text, default="")
    duration: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(50), default="draft", index=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class GoalEvidence(Base):
    __tablename__ = "goal_evidence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), index=True)
    goal_number: Mapped[int] = mapped_column(Integer, default=0)
    date: Mapped[str] = mapped_column(String(50), default="")
    season: Mapped[str] = mapped_column(String(50), default="")
    team: Mapped[str] = mapped_column(String(200), default="")
    opponent: Mapped[str] = mapped_column(String(200), default="")
    competition: Mapped[str] = mapped_column(String(200), default="")
    minute: Mapped[str] = mapped_column(String(50), default="")
    score: Mapped[str] = mapped_column(String(100), default="")
    goal_type: Mapped[str] = mapped_column(String(100), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    video_url: Mapped[str] = mapped_column(String(1000), default="")
    source_url: Mapped[str] = mapped_column(String(1000), default="")
    evidence_type: Mapped[str] = mapped_column(String(100), default="")
    verified: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    youtube_video_id: Mapped[str] = mapped_column(String(100), default="")
    youtube_timestamp: Mapped[str] = mapped_column(String(50), default="")
    youtube_channel: Mapped[str] = mapped_column(String(200), default="")
    youtube_title: Mapped[str] = mapped_column(String(500), default="")
    evidence_notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ResearchSource(Base):
    __tablename__ = "research_sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(500))
    url: Mapped[str] = mapped_column(String(1500), default="")
    source_type: Mapped[str] = mapped_column(String(100), default="web")
    publisher: Mapped[str] = mapped_column(String(300), default="")
    notes: Mapped[str] = mapped_column(Text, default="")
    reliability: Mapped[str] = mapped_column(String(50), default="unrated")
    verified: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ProductionProject(Base):
    __tablename__ = "production_projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(300))
    description: Mapped[str] = mapped_column(Text, default="")
    project_type: Mapped[str] = mapped_column(String(100), default="football_story")
    status: Mapped[str] = mapped_column(String(50), default="planning", index=True)
    aspect_ratio: Mapped[str] = mapped_column(String(30), default="16:9")
    target_platform: Mapped[str] = mapped_column(String(100), default="YouTube")
    duration_seconds: Mapped[int] = mapped_column(Integer, default=60)
    story_id: Mapped[int | None] = mapped_column(ForeignKey("stories.id"), nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ProductionScene(Base):
    __tablename__ = "production_scenes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("production_projects.id"), index=True)
    scene_number: Mapped[int] = mapped_column(Integer, default=1)
    title: Mapped[str] = mapped_column(String(300))
    description: Mapped[str] = mapped_column(Text, default="")
    narration: Mapped[str] = mapped_column(Text, default="")
    visual_prompt: Mapped[str] = mapped_column(Text, default="")
    duration_seconds: Mapped[int] = mapped_column(Integer, default=5)
    status: Mapped[str] = mapped_column(String(50), default="draft")
    asset_url: Mapped[str] = mapped_column(String(1500), default="")
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())


class SourceLink(Base):
    __tablename__ = "source_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("research_sources.id"), index=True)
    entity_type: Mapped[str] = mapped_column(String(100))
    entity_id: Mapped[int] = mapped_column(Integer, index=True)
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
