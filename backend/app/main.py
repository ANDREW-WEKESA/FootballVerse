from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import (
    engine,
    Base,
    Player,
    PlayerSeasonStat,
    PlayerHonour,
    SessionLocal,
)

from .services.thesportsdb import (
    search_player,
    get_player_stats,
    get_player_honours,
)

Base.metadata.create_all(engine)

app = FastAPI(
    title="FootballVerse API",
    version="1.6.0",
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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "system": "FootballVerse",
        "status": "running",
        "version": "1.6.0",
    }


@app.get("/players")
def all_players(db: Session = Depends(get_db)):
    return db.query(Player).order_by(Player.full_name).all()


@app.get("/players/{player_id}")
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()

    if not player:
        raise HTTPException(
            status_code=404,
            detail="Player not found",
        )

    return player


@app.get("/players/search")
def search_players(
    name: str = Query(..., min_length=2),
):
    return search_player(name)


@app.get("/players/{player_id}/history")
def player_history(
    player_id: int,
    db: Session = Depends(get_db),
):
    player = db.query(Player).filter(Player.id == player_id).first()

    if not player:
        raise HTTPException(
            status_code=404,
            detail="Player not found",
        )

    stats = (
        db.query(PlayerSeasonStat)
        .filter(PlayerSeasonStat.player_id == player.id)
        .order_by(PlayerSeasonStat.season)
        .all()
    )

    honours = (
        db.query(PlayerHonour)
        .filter(PlayerHonour.player_id == player.id)
        .order_by(PlayerHonour.season)
        .all()
    )

    return {
        "player": player,
        "season_stats": stats,
        "honours": honours,
    }


@app.post("/players/import")
def import_player(
    name: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
):
    result = search_player(name)

    players = result.get("player") or []

    if not players:
        raise HTTPException(
            status_code=404,
            detail=f"No real player found for '{name}'",
        )

    data = players[0]
    external_id = str(data.get("idPlayer", ""))

    existing = (
        db.query(Player)
        .filter(Player.external_id == external_id)
        .first()
    )

    stats_result = get_player_stats(external_id)
    honours_result = get_player_honours(external_id)

    stats = stats_result.get("playerstats") or []
    honours = honours_result.get("honours") or []

    goals = 0
    appearances = 0
    minutes = 0

    for row in stats:
        statistic = row.get("strStatistic")
        value = row.get("strValue") or "0"

        try:
            number = int(float(value))
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
        player.image_url = (
            data.get("strThumb")
            or data.get("strCutout")
            or player.image_url
        )

        player.goals = goals
        player.appearances = appearances
        player.trophies = trophies

        db.query(PlayerSeasonStat).filter(
            PlayerSeasonStat.player_id == player.id
        ).delete()

        db.query(PlayerHonour).filter(
            PlayerHonour.player_id == player.id
        ).delete()

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
        stat = PlayerSeasonStat(
            player_id=player.id,
            external_stat_id=str(row.get("id") or ""),
            season=row.get("strSeason") or "",
            team=row.get("strTeam") or "",
            league=row.get("strLeague") or "",
            statistic=row.get("strStatistic") or "",
            value=row.get("strValue") or "",
            team_badge_url=row.get("strTeamBadge") or "",
            league_badge_url=row.get("strLeagueBadge") or "",
        )

        db.add(stat)

    for row in honours:
        honour = PlayerHonour(
            player_id=player.id,
            external_honour_id=str(row.get("id") or ""),
            honour=row.get("strHonour") or "",
            season=row.get("strSeason") or "",
            team=row.get("strTeam") or "",
            league=row.get("strLeague") or "",
            honour_logo_url=row.get("strHonourLogo") or "",
            trophy_url=row.get("strHonourTrophy") or "",
            team_badge_url=row.get("strTeamBadge") or "",
        )

        db.add(honour)

    db.commit()
    db.refresh(player)

    return {
        "message": "Player history imported successfully",
        "player": player,
        "stats": {
            "goals": goals,
            "appearances": appearances,
            "minutes": minutes,
            "season_records": len(stats),
        },
        "honours": {
            "total": trophies,
            "records": len(honours),
        },
    }

@app.get("/players/{player_id}/timeline")
def player_timeline(
    player_id: int,
    db: Session = Depends(get_db),
):
    player = db.query(Player).filter(Player.id == player_id).first()

    if not player:
        raise HTTPException(
            status_code=404,
            detail="Player not found",
        )

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

    seasons = {}

    for stat in season_stats:
        season = stat.season or "Unknown"

        if season not in seasons:
            seasons[season] = {
                "season": season,
                "teams": set(),
                "leagues": set(),
                "appearances": 0,
                "goals": 0,
                "minutes": 0,
            }

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

    timeline = []

    for season, data in seasons.items():
        timeline.append({
            "season": season,
            "teams": sorted(x for x in data["teams"] if x),
            "leagues": sorted(x for x in data["leagues"] if x),
            "appearances": data["appearances"],
            "goals": data["goals"],
            "minutes": data["minutes"],
        })

    honour_timeline = [
        {
            "season": honour.season,
            "honour": honour.honour,
            "team": honour.team,
            "league": honour.league,
            "honour_logo_url": honour.honour_logo_url,
            "trophy_url": honour.trophy_url,
            "team_badge_url": honour.team_badge_url,
        }
        for honour in honours
    ]

    return {
        "player": player,
        "career_timeline": timeline,
        "honours_timeline": honour_timeline,
    }

@app.get("/players/{player_id}/story")
def player_story(
    player_id: int,
    db: Session = Depends(get_db),
):
    player = db.query(Player).filter(Player.id == player_id).first()

    if not player:
        raise HTTPException(
            status_code=404,
            detail="Player not found",
        )

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

    events = []

    for stat in season_stats:
        events.append({
            "year": stat.season,
            "type": "career",
            "title": f"{stat.team} - {stat.league}",
            "description": (
                f"{stat.statistic}: {stat.value}"
            ),
            "team": stat.team,
            "league": stat.league,
            "team_badge_url": stat.team_badge_url,
            "league_badge_url": stat.league_badge_url,
        })

    for honour in honours:
        events.append({
            "year": honour.season,
            "type": "honour",
            "title": honour.honour,
            "description": (
                f"{honour.honour} with {honour.team}"
                if honour.team
                else honour.honour
            ),
            "team": honour.team,
            "league": honour.league,
            "honour_logo_url": honour.honour_logo_url,
            "trophy_url": honour.trophy_url,
            "team_badge_url": honour.team_badge_url,
        })

    events.sort(key=lambda x: str(x["year"]))

    return {
        "player": {
            "id": player.id,
            "name": player.full_name,
            "nationality": player.nationality,
            "position": player.position,
            "date_of_birth": player.date_of_birth,
            "image_url": player.image_url,
        },
        "title": f"The Story of {player.full_name}",
        "intro": (
            f"Follow the football journey of {player.full_name}, "
            f"from the early stages of their career through "
            f"the major moments recorded in FootballVerse."
        ),
        "events": events,
        "event_count": len(events),
    }

