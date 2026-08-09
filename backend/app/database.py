from sqlalchemy import create_engine, Integer, String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

DATABASE_URL = "sqlite:///./footballverse.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    external_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        default=""
    )

    full_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    nationality: Mapped[str] = mapped_column(
        String(100),
        default=""
    )

    date_of_birth: Mapped[str] = mapped_column(
        String(50),
        default=""
    )

    position: Mapped[str] = mapped_column(
        String(100),
        default=""
    )

    image_url: Mapped[str] = mapped_column(
        String(500),
        default=""
    )

    biography: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    career_summary: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    international_career: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    goals: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    appearances: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    assists: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    trophies: Mapped[int] = mapped_column(
        Integer,
        default=0
    )


class PlayerSeasonStat(Base):
    __tablename__ = "player_season_stats"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=False,
        index=True
    )

    external_stat_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        default=""
    )

    season: Mapped[str] = mapped_column(
        String(50),
        default=""
    )

    team: Mapped[str] = mapped_column(
        String(200),
        default=""
    )

    league: Mapped[str] = mapped_column(
        String(200),
        default=""
    )

    statistic: Mapped[str] = mapped_column(
        String(100),
        default=""
    )

    value: Mapped[str] = mapped_column(
        String(100),
        default=""
    )

    team_badge_url: Mapped[str] = mapped_column(
        String(500),
        default=""
    )

    league_badge_url: Mapped[str] = mapped_column(
        String(500),
        default=""
    )


class PlayerHonour(Base):
    __tablename__ = "player_honours"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=False,
        index=True
    )

    external_honour_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        default=""
    )

    honour: Mapped[str] = mapped_column(
        String(200),
        default=""
    )

    season: Mapped[str] = mapped_column(
        String(50),
        default=""
    )

    team: Mapped[str] = mapped_column(
        String(200),
        default=""
    )

    league: Mapped[str] = mapped_column(
        String(200),
        default=""
    )

    honour_logo_url: Mapped[str] = mapped_column(
        String(500),
        default=""
    )

    trophy_url: Mapped[str] = mapped_column(
        String(500),
        default=""
    )

    team_badge_url: Mapped[str] = mapped_column(
        String(500),
        default=""
    )


Base.metadata.create_all(engine)

print("=== FOOTBALLVERSE DATABASE READY ===")
print("Database: footballverse.db")
print("Tables: players, player_season_stats, player_honours")

class PlayerGoal(Base):
    __tablename__ = "player_goals"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=False,
        index=True
    )

    goal_number: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    date: Mapped[str] = mapped_column(
        String(50),
        default=""
    )

    season: Mapped[str] = mapped_column(
        String(50),
        default=""
    )

    team: Mapped[str] = mapped_column(
        String(200),
        default=""
    )

    opponent: Mapped[str] = mapped_column(
        String(200),
        default=""
    )

    competition: Mapped[str] = mapped_column(
        String(200),
        default=""
    )

    minute: Mapped[str] = mapped_column(
        String(50),
        default=""
    )

    score: Mapped[str] = mapped_column(
        String(100),
        default=""
    )

    goal_type: Mapped[str] = mapped_column(
        String(100),
        default=""
    )

    description: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    video_url: Mapped[str] = mapped_column(
        String(1000),
        default=""
    )

    source_url: Mapped[str] = mapped_column(
        String(1000),
        default=""
    )

    evidence_type: Mapped[str] = mapped_column(
        String(100),
        default=""
    )

    verified: Mapped[bool] = mapped_column(
        default=False
    )

    youtube_video_id: Mapped[str] = mapped_column(
        String(100),
        default=""
    )

    youtube_timestamp: Mapped[str] = mapped_column(
        String(50),
        default=""
    )

    youtube_channel: Mapped[str] = mapped_column(
        String(200),
        default=""
    )

    youtube_title: Mapped[str] = mapped_column(
        String(500),
        default=""
    )

    evidence_notes: Mapped[str] = mapped_column(
        Text,
        default=""
    )
