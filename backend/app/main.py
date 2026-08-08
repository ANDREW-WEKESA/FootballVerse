from fastapi import FastAPI
from .database import stories, players, clubs, media, scenes

app = FastAPI(title="FootballVerse Full System")

@app.get("/")
def home():
    return {"system":"FootballVerse","status":"running"}

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

@app.get("/media")
def all_media():
    return media

@app.get("/stories/{story_id}/scenes")
def story_scenes(story_id:int):
    return scenes
