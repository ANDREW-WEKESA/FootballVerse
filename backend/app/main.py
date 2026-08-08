from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import stories, players, clubs, media, scenes

competitions = []
achievements = []

app = FastAPI(title="FootballVerse Full System", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "system": "FootballVerse",
        "status": "running",
        "version": "1.1.0"
    }

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

@app.get("/clubs")
def all_clubs():
    return clubs

@app.get("/competitions")
def all_competitions():
    return competitions

@app.post("/competitions")
def create_competition(competition: dict):
    competitions.append(competition)
    return competition

@app.get("/achievements")
def all_achievements():
    return achievements

@app.post("/achievements")
def create_achievement(achievement: dict):
    achievements.append(achievement)
    return achievement

@app.get("/media")
def all_media():
    return media

@app.get("/stories/{story_id}/scenes")
def story_scenes(story_id: int):
    return scenes
