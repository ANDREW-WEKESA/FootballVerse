from fastapi import FastAPI

app = FastAPI(
    title="FootballVerse",
    version="0.1"
)

@app.get("/")
def root():
    return {
        "project":"FootballVerse",
        "status":"online",
        "version":"0.1"
    }

@app.get("/health")
def health():
    return {
        "ok":True
    }
