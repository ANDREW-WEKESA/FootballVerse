import os
import sys
import logging

from sqlalchemy import (
    create_engine,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    JSON,
    DateTime,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.sql import func
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable is not set. Exiting.")
    sys.exit(1)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    email: Mapped[str] = mapped_column(
        String(254),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
    )

    is_admin: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


# ---------------------------------------------------------------------------
# Club
# ---------------------------------------------------------------------------

class Club(Base):
    __tablename__ = "clubs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    founded_year: Mapped[int] = mapped_column(Integer, nullable=True)

    stadium: Mapped[str] = mapped_column(String(200), default="")

    trophies: Mapped[int] = mapped_column(Integer, default=0)

    logo_url: Mapped[str] = mapped_column(String(500), default="")

    description: Mapped[str] = mapped_column(Text, default="")

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


# ---------------------------------------------------------------------------
# Player
# ---------------------------------------------------------------------------

class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    external_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        default="",
    )

    full_name: Mapped[str] = mapped_column(String(200), nullable=False)

    nationality: Mapped[str] = mapped_column(String(100), default="")

    date_of_birth: Mapped[str] = mapped_column(String(50), default="")

    position: Mapped[str] = mapped_column(String(100), default="")

    image_url: Mapped[str] = mapped_column(String(500), default="")

    biography: Mapped[str] = mapped_column(Text, default="")

    career_summary: Mapped[str] = mapped_column(Text, default="")

    international_career: Mapped[str] = mapped_column(Text, default="")

    goals: Mapped[int] = mapped_column(Integer, default=0)

    appearances: Mapped[int] = mapped_column(Integer, default=0)

    assists: Mapped[int] = mapped_column(Integer, default=0)

    trophies: Mapped[int] = mapped_column(Integer, default=0)


# ---------------------------------------------------------------------------
# Story
# ---------------------------------------------------------------------------

class Story(Base):
    __tablename__ = "stories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(String(300), nullable=False)

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=True,
        index=True,
    )

    club_id: Mapped[int] = mapped_column(
        ForeignKey("clubs.id"),
        nullable=True,
        index=True,
    )

    script: Mapped[str] = mapped_column(Text, default="")

    media_metadata: Mapped[dict] = mapped_column(JSON, default=dict)

    source_rights_metadata: Mapped[dict] = mapped_column(JSON, default=dict)

    narration_file: Mapped[str] = mapped_column(String(500), default="")

    status: Mapped[str] = mapped_column(
        String(20),
        default="draft",
        index=True,
    )

    render_output_path: Mapped[str] = mapped_column(String(500), default="")

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


# ---------------------------------------------------------------------------
# PlayerSeasonStat
# ---------------------------------------------------------------------------

class PlayerSeasonStat(Base):
    __tablename__ = "player_season_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=False,
        index=True,
    )

    external_stat_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        default="",
    )

    season: Mapped[str] = mapped_column(String(50), default="")

    team: Mapped[str] = mapped_column(String(200), default="")

    league: Mapped[str] = mapped_column(String(200), default="")

    statistic: Mapped[str] = mapped_column(String(100), default="")

    value: Mapped[str] = mapped_column(String(100), default="")

    team_badge_url: Mapped[str] = mapped_column(String(500), default="")

    league_badge_url: Mapped[str] = mapped_column(String(500), default="")


# ---------------------------------------------------------------------------
# PlayerHonour
# ---------------------------------------------------------------------------

class PlayerHonour(Base):
    __tablename__ = "player_honours"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=False,
        index=True,
    )

    external_honour_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        default="",
    )

    honour: Mapped[str] = mapped_column(String(200), default="")

    season: Mapped[str] = mapped_column(String(50), default="")

    team: Mapped[str] = mapped_column(String(200), default="")

    league: Mapped[str] = mapped_column(String(200), default="")

    honour_logo_url: Mapped[str] = mapped_column(String(500), default="")

    trophy_url: Mapped[str] = mapped_column(String(500), default="")

    team_badge_url: Mapped[str] = mapped_column(String(500), default="")


# ---------------------------------------------------------------------------
# PlayerGoal
# ---------------------------------------------------------------------------

class PlayerGoal(Base):
    __tablename__ = "player_goals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=False,
        index=True,
    )

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

    verified: Mapped[bool] = mapped_column(Boolean, default=False)

    youtube_video_id: Mapped[str] = mapped_column(String(100), default="")

    youtube_timestamp: Mapped[str] = mapped_column(String(50), default="")

    youtube_channel: Mapped[str] = mapped_column(String(200), default="")

    youtube_title: Mapped[str] = mapped_column(String(500), default="")

    evidence_notes: Mapped[str] = mapped_column(Text, default="")
