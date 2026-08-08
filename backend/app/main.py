from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import stories, players, clubs, media, scenes

competitions = []
achievements = []
player_profiles = []

app = FastAPI(title="FootballVerse Full System", version="1.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"system": "FootballVerse", "status": "running", "version": "1.2.0"}

@app.get("/stories")
def all_stories():
    return stories

@app.post("/stories")
def create_story(story: dict):
    stories.append(story)
    return story

@app.get("/players")
def all_players():
    return players

@app.get("/players/{player_id}")
def player_profile(player_id: int):
    if player_id < len(player_profiles):
        return player_profiles[player_id]
    return {"id": player_id, "message": "Player profile not found"}

@app.post("/players")
def create_player(player: dict):
    player["id"] = len(player_profiles)
    player_profiles.append(player)
    return player

@app.get("/clubs")
def all_clubs():
    return clubs

@app.get("/competitions")
def all_competitions():
    return competitions

@app.post("/competitions")
def create_competition(competition: dict):
    competition["id"] = len(competitions)
    competitions.append(competition)
    return competition

@app.get("/achievements")
def all_achievements():
    return achievements

@app.post("/achievements")
def create_achievement(achievement: dict):
    achievement["id"] = len(achievements)
    achievements.append(achievement)
    return achievement

@app.get("/media")
def all_media():
    return media

@app.get("/stories/{story_id}/scenes")
def story_scenes(story_id: int):
    return scenes
