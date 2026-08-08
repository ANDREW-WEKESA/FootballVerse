from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, Player

app = FastAPI(title="FootballVerse Full System", version="1.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        "version": "1.3.0"
    }

@app.get("/players")
def all_players(db: Session = Depends(get_db)):
    return db.query(Player).all()

@app.get("/players/{player_id}")
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()

    if not player:
        return {"error": "Player not found"}

    return player

@app.post("/players")
def create_player(player: dict, db: Session = Depends(get_db)):
    new_player = Player(
        full_name=player.get("full_name", ""),
        nationality=player.get("nationality", ""),
        date_of_birth=player.get("date_of_birth", ""),
        position=player.get("position", ""),
        biography=player.get("biography", ""),
        career_summary=player.get("career_summary", ""),
        international_career=player.get("international_career", ""),
        goals=player.get("goals", 0),
        appearances=player.get("appearances", 0),
        assists=player.get("assists", 0),
        trophies=player.get("trophies", 0)
    )

    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    return new_player
