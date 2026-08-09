import logging
import os

from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, field_validator, model_validator
from sqlalchemy.orm import Session
from sqlalchemy import func

from .database import (
    Base,
    Club,
    Player,
    PlayerGoal,
    PlayerHonour,
    PlayerSeasonStat,
    Story,
    engine,
)
from .auth import (
    create_access_token,
    ensure_admin_exists,
    get_current_admin,
    get_db,
    get_optional_current_user,
    get_user_by_email,
    verify_password,
)
from .services.thesportsdb import (
    get_player_honours,
    get_player_stats,
    search_player,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(engine)

app = FastAPI(
    title="FootballVerse API",
    version="2.0.0",
    description="Football knowledge and storytelling platform API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    db = next(get_db())
    try:
        ensure_admin_exists(db)
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

class LoginRequest(BaseModel):
    email: str
    password: str


class ClubCreate(BaseModel):
    name: str
    country: str
    founded_year: int | None = None
    stadium: str = ""
    trophies: int = 0
    logo_url: str = ""
    description: str = ""


class ClubUpdate(BaseModel):
    name: str | None = None
    country: str | None = None
    founded_year: int | None = None
    stadium: str | None = None
    trophies: int | None = None
    logo_url: str | None = None
    description: str | None = None


VALID_STATUSES = {"draft", "rendered", "published"}


class StoryCreate(BaseModel):
    title: str
    player_id: int | None = None
    club_id: int | None = None
    script: str = ""
    media_metadata: dict = {}
    source_rights_metadata: dict = {}
    narration_file: str = ""
    status: str = "draft"

    @model_validator(mode="after")
    def requires_player_or_club(self):
        if not self.player_id and not self.club_id:
            raise ValueError("A story must be linked to a player_id or club_id.")
        return self

    @field_validator("status")
    @classmethod
    def valid_status(cls, v):
        if v not in VALID_STATUSES:
            raise ValueError(f"status must be one of {VALID_STATUSES}")
        return v


class StoryUpdate(BaseModel):
    title: str | None = None
    script: str | None = None
    media_metadata: dict | None = None
    source_rights_metadata: dict | None = None
    narration_file: str | None = None
    status: str | None = None
    player_id: int | None = None
    club_id: int | None = None

    @field_validator("status")
    @classmethod
    def valid_status(cls, v):
        if v is not None and v not in VALID_STATUSES:
            raise ValueError(f"status must be one of {VALID_STATUSES}")
        return v


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@app.get("/", tags=["health"], summary="API health check")
def home():
    return {"system": "FootballVerse", "status": "running", "version": "2.0.0"}


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

@app.post("/auth/login", tags=["auth"], summary="Admin login — returns JWT")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    if len(body.email) > 254 or len(body.password) > 72:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    user = get_user_by_email(db, body.email)
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}


# ---------------------------------------------------------------------------
# Clubs
# ---------------------------------------------------------------------------

@app.get("/clubs", tags=["clubs"], summary="List all clubs")
def list_clubs(
    search: str | None = Query(None, min_length=2),
    db: Session = Depends(get_db),
):
    q = db.query(Club)
    if search:
        q = q.filter(Club.name.ilike(f"%{search}%"))
    return q.order_by(Club.name).all()


@app.get("/clubs/{club_id}", tags=["clubs"], summary="Get a club by ID")
def get_club(club_id: int, db: Session = Depends(get_db)):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    return club


@app.post("/clubs", tags=["clubs"], summary="Create a club (admin)", status_code=201)
def create_club(
    body: ClubCreate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    club = Club(**body.model_dump())
    db.add(club)
    db.commit()
    db.refresh(club)
    return club


@app.put("/clubs/{club_id}", tags=["clubs"], summary="Update a club (admin)")
def update_club(
    club_id: int,
    body: ClubUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(club, field, value)
    db.commit()
    db.refresh(club)
    return club


@app.delete("/clubs/{club_id}", tags=["clubs"], summary="Delete a club (admin)")
def delete_club(
    club_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    linked = db.query(Story).filter(Story.club_id == club_id).first()
    if linked:
        raise HTTPException(
            status_code=409,
            detail="Club has linked stories — remove them first",
        )
    db.delete(club)
    db.commit()
    return {"status": "deleted", "club_id": club_id}


# ---------------------------------------------------------------------------
# Stories
# ---------------------------------------------------------------------------

@app.get("/stories", tags=["stories"], summary="List stories")
def list_stories(
    db: Session = Depends(get_db),
    current_user=Depends(get_optional_current_user),
):
    q = db.query(Story)
    if not current_user:
        q = q.filter(Story.status == "published")
    return q.order_by(Story.created_at.desc()).all()


@app.get("/stories/{story_id}", tags=["stories"], summary="Get a story by ID")
def get_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@app.post("/stories", tags=["stories"], summary="Create a story (admin)", status_code=201)
def create_story(
    body: StoryCreate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    if body.player_id:
        if not db.query(Player).filter(Player.id == body.player_id).first():
            raise HTTPException(status_code=404, detail="Player not found")
    if body.club_id:
        if not db.query(Club).filter(Club.id == body.club_id).first():
            raise HTTPException(status_code=404, detail="Club not found")
    story = Story(**body.model_dump())
    db.add(story)
    db.commit()
    db.refresh(story)
    return story


@app.put("/stories/{story_id}", tags=["stories"], summary="Update a story (admin)")
def update_story(
    story_id: int,
    body: StoryUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(story, field, value)
    db.commit()
    db.refresh(story)
    return story


@app.delete("/stories/{story_id}", tags=["stories"], summary="Delete a story (admin)")
def delete_story(
    story_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    db.delete(story)
    db.commit()
    return {"status": "deleted", "story_id": story_id}


# ---------------------------------------------------------------------------
# Render / Download stubs (wired up in Phase 3)
# ---------------------------------------------------------------------------

@app.post("/stories/{story_id}/render", tags=["stories"], summary="Trigger render (admin)")
def render_story(
    story_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    if story.status != "draft":
        raise HTTPException(status_code=409, detail="Only draft stories can be rendered")
    # Pipeline wired in Phase 3 — placeholder returns accepted
    return {"status": "accepted", "story_id": story_id, "message": "Render pipeline coming in Phase 3"}


@app.get("/stories/{story_id}/download", tags=["stories"], summary="Download rendered video")
def download_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    if not story.render_output_path:
        raise HTTPException(status_code=404, detail="No rendered output for this story")
    return {"download_url": f"/videos/{os.path.basename(story.render_output_path)}"}


# ---------------------------------------------------------------------------
# Players
# ---------------------------------------------------------------------------

@app.get("/players", tags=["players"], summary="List all players")
def all_players(
    search: str | None = Query(None, min_length=2),
    db: Session = Depends(get_db),
):
    q = db.query(Player)
    if search:
        q = q.filter(Player.full_name.ilike(f"%{search}%"))
    return q.order_by(Player.full_name).all()


@app.get("/players/{player_id}", tags=["players"], summary="Get a player by ID")
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@app.get("/players/{player_id}/history", tags=["players"], summary="Player career history")
def player_history(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    stats = (
        db.query(PlayerSeasonStat)
        .filter(PlayerSeasonStat.player_id == player_id)
        .order_by(PlayerSeasonStat.season)
        .all()
    )
    honours = (
        db.query(PlayerHonour)
        .filter(PlayerHonour.player_id == player_id)
        .order_by(PlayerHonour.season)
        .all()
    )
    return {"player": player, "season_stats": stats, "honours": honours}


@app.post("/players/import", tags=["players"], summary="Import player from TheSportsDB")
def import_player(
    name: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
):
    result = search_player(name)
    players = result.get("player") or []
    if not players:
        raise HTTPException(status_code=404, detail=f"No player found for '{name}'")

    data = players[0]
    external_id = str(data.get("idPlayer", ""))
    existing = db.query(Player).filter(Player.external_id == external_id).first()

    stats_result = get_player_stats(external_id)
    honours_result = get_player_honours(external_id)
    stats = stats_result.get("playerstats") or []
    honours = honours_result.get("honours") or []

    goals = appearances = minutes = 0
    for row in stats:
        statistic = row.get("strStatistic")
        try:
            number = int(float(row.get("strValue") or "0"))
        except (ValueError, TypeError):
            number = 0
        if statistic == "Goals":
            goals += number
        elif statistic == "Appearances":
            appearances += number
        elif statistic == "Mins Played":
            minutes += number

    trophies = len(honours)

    if existing:
        player = existing
        player.full_name = data.get("strPlayer") or player.full_name
        player.nationality = data.get("strNationality") or player.nationality
        player.date_of_birth = data.get("dateBorn") or player.date_of_birth
        player.position = data.get("strPosition") or player.position
        player.image_url = data.get("strThumb") or data.get("strCutout") or player.image_url
        player.goals = goals
        player.appearances = appearances
        player.trophies = trophies
        db.query(PlayerSeasonStat).filter(PlayerSeasonStat.player_id == player.id).delete()
        db.query(PlayerHonour).filter(PlayerHonour.player_id == player.id).delete()
    else:
        player = Player(
            external_id=external_id,
            full_name=data.get("strPlayer") or name,
            nationality=data.get("strNationality") or "",
            date_of_birth=data.get("dateBorn") or "",
            position=data.get("strPosition") or "",
            image_url=data.get("strThumb") or data.get("strCutout") or "",
            biography="",
            career_summary="",
            international_career="",
            goals=goals,
            appearances=appearances,
            assists=0,
            trophies=trophies,
        )
        db.add(player)
        db.flush()

    for row in stats:
        db.add(PlayerSeasonStat(
            player_id=player.id,
            external_stat_id=str(row.get("id") or ""),
            season=row.get("strSeason") or "",
            team=row.get("strTeam") or "",
            league=row.get("strLeague") or "",
            statistic=row.get("strStatistic") or "",
            value=row.get("strValue") or "",
            team_badge_url=row.get("strTeamBadge") or "",
            league_badge_url=row.get("strLeagueBadge") or "",
        ))

    for row in honours:
        db.add(PlayerHonour(
            player_id=player.id,
            external_honour_id=str(row.get("id") or ""),
            honour=row.get("strHonour") or "",
            season=row.get("strSeason") or "",
            team=row.get("strTeam") or "",
            league=row.get("strLeague") or "",
            honour_logo_url=row.get("strHonourLogo") or "",
            trophy_url=row.get("strHonourTrophy") or "",
            team_badge_url=row.get("strTeamBadge") or "",
        ))

    db.commit()
    db.refresh(player)
    return {
        "message": "Player imported successfully",
        "player": player,
        "stats": {"goals": goals, "appearances": appearances, "minutes": minutes, "season_records": len(stats)},
        "honours": {"total": trophies, "records": len(honours)},
    }


@app.get("/players/{player_id}/timeline", tags=["players"], summary="Player career timeline")
def player_timeline(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    season_stats = (
        db.query(PlayerSeasonStat)
        .filter(PlayerSeasonStat.player_id == player_id)
        .order_by(PlayerSeasonStat.season.asc())
        .all()
    )
    honours = (
        db.query(PlayerHonour)
        .filter(PlayerHonour.player_id == player_id)
        .order_by(PlayerHonour.season.asc())
        .all()
    )

    seasons: dict = {}
    for stat in season_stats:
        season = stat.season or "Unknown"
        if season not in seasons:
            seasons[season] = {"season": season, "teams": set(), "leagues": set(), "appearances": 0, "goals": 0, "minutes": 0}
        seasons[season]["teams"].add(stat.team or "")
        seasons[season]["leagues"].add(stat.league or "")
        try:
            value = int(float(stat.value or 0))
        except (ValueError, TypeError):
            value = 0
        if stat.statistic == "Appearances":
            seasons[season]["appearances"] += value
        elif stat.statistic == "Goals":
            seasons[season]["goals"] += value
        elif stat.statistic == "Mins Played":
            seasons[season]["minutes"] += value

    timeline = [
        {
            "season": d["season"],
            "teams": sorted(x for x in d["teams"] if x),
            "leagues": sorted(x for x in d["leagues"] if x),
            "appearances": d["appearances"],
            "goals": d["goals"],
            "minutes": d["minutes"],
        }
        for d in seasons.values()
    ]

    honour_timeline = [
        {
            "season": h.season, "honour": h.honour, "team": h.team, "league": h.league,
            "honour_logo_url": h.honour_logo_url, "trophy_url": h.trophy_url, "team_badge_url": h.team_badge_url,
        }
        for h in honours
    ]

    return {"player": player, "career_timeline": timeline, "honours_timeline": honour_timeline}


@app.get("/players/{player_id}/story", tags=["players"], summary="Player story events")
def player_story(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    season_stats = db.query(PlayerSeasonStat).filter(PlayerSeasonStat.player_id == player_id).order_by(PlayerSeasonStat.season.asc()).all()
    honours = db.query(PlayerHonour).filter(PlayerHonour.player_id == player_id).order_by(PlayerHonour.season.asc()).all()

    events = []
    for stat in season_stats:
        events.append({"year": stat.season, "type": "career", "title": f"{stat.team} - {stat.league}", "description": f"{stat.statistic}: {stat.value}", "team": stat.team, "league": stat.league, "team_badge_url": stat.team_badge_url, "league_badge_url": stat.league_badge_url})
    for honour in honours:
        events.append({"year": honour.season, "type": "honour", "title": honour.honour, "description": f"{honour.honour} with {honour.team}" if honour.team else honour.honour, "team": honour.team, "league": honour.league, "honour_logo_url": honour.honour_logo_url, "trophy_url": honour.trophy_url, "team_badge_url": honour.team_badge_url})
    events.sort(key=lambda x: str(x["year"]))

    return {
        "player": {"id": player.id, "name": player.full_name, "nationality": player.nationality, "position": player.position, "date_of_birth": player.date_of_birth, "image_url": player.image_url},
        "title": f"The Story of {player.full_name}",
        "intro": f"Follow the football journey of {player.full_name}, from the early stages of their career through the major moments recorded in FootballVerse.",
        "events": events,
        "event_count": len(events),
    }


@app.get("/players/{player_id}/goals", tags=["players"], summary="Player goals")
def get_player_goals(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    goals = db.query(PlayerGoal).filter(PlayerGoal.player_id == player_id).order_by(PlayerGoal.date, PlayerGoal.goal_number).all()
    return {"player": player, "goal_count": len(goals), "goals": goals}


@app.post("/players/{player_id}/goals", tags=["players"], summary="Add a goal", status_code=201)
def add_player_goal(player_id: int, goal: dict, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    new_goal = PlayerGoal(player_id=player_id, **{k: goal.get(k, "") for k in ["date","season","team","opponent","competition","minute","score","goal_type","description","video_url","source_url","evidence_type"]}, goal_number=goal.get("goal_number", 0), verified=goal.get("verified", False))
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return new_goal


@app.delete("/players/{player_id}/goals/{goal_id}", tags=["players"], summary="Delete a goal")
def delete_player_goal(player_id: int, goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(PlayerGoal).filter(PlayerGoal.id == goal_id, PlayerGoal.player_id == player_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(goal)
    db.commit()
    return {"status": "deleted", "goal_id": goal_id}


@app.put("/players/{player_id}/goals/{goal_id}/evidence", tags=["players"], summary="Update goal evidence")
def update_goal_evidence(player_id: int, goal_id: int, evidence: dict, db: Session = Depends(get_db)):
    goal = db.query(PlayerGoal).filter(PlayerGoal.id == goal_id, PlayerGoal.player_id == player_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    for field in ["video_url","source_url","evidence_type","youtube_video_id","youtube_timestamp","youtube_channel","youtube_title","evidence_notes"]:
        if field in evidence:
            setattr(goal, field, evidence[field])
    if "verified" in evidence:
        goal.verified = bool(evidence["verified"])
    db.commit()
    db.refresh(goal)
    return goal


@app.get("/players/{player_id}/goals/{goal_id}/evidence", tags=["players"], summary="Get goal evidence")
def get_goal_evidence(player_id: int, goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(PlayerGoal).filter(PlayerGoal.id == goal_id, PlayerGoal.player_id == player_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {"goal_id": goal.id, "player_id": goal.player_id, "goal_number": goal.goal_number, "match": {"date": goal.date, "season": goal.season, "team": goal.team, "opponent": goal.opponent, "competition": goal.competition, "minute": goal.minute, "score": goal.score}, "evidence": {"type": goal.evidence_type, "verified": goal.verified, "video_url": goal.video_url, "source_url": goal.source_url, "youtube_video_id": goal.youtube_video_id, "youtube_timestamp": goal.youtube_timestamp, "youtube_channel": goal.youtube_channel, "youtube_title": goal.youtube_title, "notes": goal.evidence_notes}}


app.mount("/videos", StaticFiles(directory="static/videos"), name="videos")
