from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import engine, Base, Player
from .services.thesportsdb import search_player

Base.metadata.create_all(engine)

app = FastAPI(
    title="FootballVerse API",
    version="1.4.0"
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
    from .database import SessionLocal

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
        "version": "1.4.0"
    }


@app.get("/players")
def all_players(db: Session = Depends(get_db)):
    return db.query(Player).order_by(Player.full_name).all()


@app.get("/players/{player_id}")
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    return player


@app.get("/players/search")
def search_players(
    name: str = Query(..., min_length=2),
):
    return search_player(name)


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
            detail=f"No real player found for '{name}'"
        )

    data = players[0]

    external_id = str(data.get("idPlayer", ""))

    existing = (
        db.query(Player)
        .filter(Player.external_id == external_id)
        .first()
    )

    if existing:
        return {
            "message": "Player already imported",
            "player": existing
        }

    new_player = Player(
        external_id=external_id,
        full_name=data.get("strPlayer") or name,
        nationality=data.get("strNationality") or "",
        date_of_birth=data.get("dateBorn") or "",
        position=data.get("strPosition") or "",
        image_url=data.get("strThumb") or data.get("strCutout") or "",
        biography="",
        career_summary="",
        international_career="",
        goals=0,
        appearances=0,
        assists=0,
        trophies=0,
    )

    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    return {
        "message": "Real player imported successfully",
        "player": new_player
    }
