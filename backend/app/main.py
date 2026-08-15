from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from .database import (
    get_db,
    init_db,
    User,
    Club,
    Player,
    Story,
    GoalEvidence,
    ResearchSource,
    ProductionProject,
    ProductionScene,
    SourceLink,
)

app = FastAPI(
    title="FootballVerse API",
    version="2.1.0",
    description="Football research, storytelling and animation production platform.",
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health", tags=["system"])
def health():
    return {
        "system": "FootballVerse",
        "status": "running",
        "version": "2.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/", tags=["system"])
def root():
    return {
        "system": "FootballVerse",
        "status": "running",
        "version": "2.1.0",
    }


class ResearchSourceCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    url: str = ""
    source_type: str = "web"
    publisher: str = ""
    notes: str = ""
    reliability: str = "unrated"
    verified: bool = False


class ResearchSourceUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    source_type: Optional[str] = None
    publisher: Optional[str] = None
    notes: Optional[str] = None
    reliability: Optional[str] = None
    verified: Optional[bool] = None


class GoalEvidenceCreate(BaseModel):
    player_id: int
    goal_number: int = 0
    date: str = ""
    season: str = ""
    team: str = ""
    opponent: str = ""
    competition: str = ""
    minute: str = ""
    score: str = ""
    goal_type: str = ""
    description: str = ""
    video_url: str = ""
    source_url: str = ""
    evidence_type: str = ""
    verified: bool = False
    youtube_video_id: str = ""
    youtube_timestamp: str = ""
    youtube_channel: str = ""
    youtube_title: str = ""
    evidence_notes: str = ""


class GoalEvidenceUpdate(BaseModel):
    verified: Optional[bool] = None
    description: Optional[str] = None
    video_url: Optional[str] = None
    source_url: Optional[str] = None
    evidence_notes: Optional[str] = None
    youtube_video_id: Optional[str] = None
    youtube_timestamp: Optional[str] = None
    youtube_channel: Optional[str] = None
    youtube_title: Optional[str] = None


class ProductionProjectCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    description: str = ""
    project_type: str = "football_story"
    status: str = "planning"
    aspect_ratio: str = "16:9"
    target_platform: str = "YouTube"
    duration_seconds: int = Field(default=60, ge=0)
    story_id: Optional[int] = None


class ProductionProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    project_type: Optional[str] = None
    status: Optional[str] = None
    aspect_ratio: Optional[str] = None
    target_platform: Optional[str] = None
    duration_seconds: Optional[int] = Field(default=None, ge=0)
    story_id: Optional[int] = None


class ProductionSceneCreate(BaseModel):
    scene_number: int = Field(default=1, ge=1)
    title: str = Field(min_length=1, max_length=300)
    description: str = ""
    narration: str = ""
    visual_prompt: str = ""
    duration_seconds: int = Field(default=5, ge=0)
    status: str = "draft"
    asset_url: str = ""


class ProductionSceneUpdate(BaseModel):
    scene_number: Optional[int] = Field(default=None, ge=1)
    title: Optional[str] = None
    description: Optional[str] = None
    narration: Optional[str] = None
    visual_prompt: Optional[str] = None
    duration_seconds: Optional[int] = Field(default=None, ge=0)
    status: Optional[str] = None
    asset_url: Optional[str] = None


def source_dict(source):
    return {
        "id": source.id,
        "title": source.title,
        "url": source.url,
        "source_type": source.source_type,
        "publisher": source.publisher,
        "notes": source.notes,
        "reliability": source.reliability,
        "verified": source.verified,
        "created_at": source.created_at,
    }


def evidence_dict(item):
    return {
        "id": item.id,
        "player_id": item.player_id,
        "goal_number": item.goal_number,
        "date": item.date,
        "season": item.season,
        "team": item.team,
        "opponent": item.opponent,
        "competition": item.competition,
        "minute": item.minute,
        "score": item.score,
        "goal_type": item.goal_type,
        "description": item.description,
        "video_url": item.video_url,
        "source_url": item.source_url,
        "evidence_type": item.evidence_type,
        "verified": item.verified,
        "youtube_video_id": item.youtube_video_id,
        "youtube_timestamp": item.youtube_timestamp,
        "youtube_channel": item.youtube_channel,
        "youtube_title": item.youtube_title,
        "evidence_notes": item.evidence_notes,
        "created_at": item.created_at,
    }


def project_dict(project):
    return {
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "project_type": project.project_type,
        "status": project.status,
        "aspect_ratio": project.aspect_ratio,
        "target_platform": project.target_platform,
        "duration_seconds": project.duration_seconds,
        "story_id": project.story_id,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
    }


def scene_dict(scene):
    return {
        "id": scene.id,
        "project_id": scene.project_id,
        "scene_number": scene.scene_number,
        "title": scene.title,
        "description": scene.description,
        "narration": scene.narration,
        "visual_prompt": scene.visual_prompt,
        "duration_seconds": scene.duration_seconds,
        "status": scene.status,
        "asset_url": scene.asset_url,
        "created_at": scene.created_at,
    }


# ---------------------------------------------------------------------------
# Research
# ---------------------------------------------------------------------------

@app.get("/research/sources", tags=["research"])
def list_sources(
    db: Session = Depends(get_db),
    verified: Optional[bool] = None,
    q: Optional[str] = Query(default=None, max_length=200),
):
    query = db.query(ResearchSource)

    if verified is not None:
        query = query.filter(ResearchSource.verified == verified)

    if q:
        query = query.filter(
            ResearchSource.title.ilike(f"%{q}%")
            | ResearchSource.publisher.ilike(f"%{q}%")
        )

    return [source_dict(x) for x in query.order_by(ResearchSource.id.desc()).all()]


@app.post("/research/sources", tags=["research"])
def create_source(body: ResearchSourceCreate, db: Session = Depends(get_db)):
    source = ResearchSource(**body.model_dump())
    db.add(source)
    db.commit()
    db.refresh(source)
    return source_dict(source)


@app.get("/research/sources/{source_id}", tags=["research"])
def get_source(source_id: int, db: Session = Depends(get_db)):
    source = db.get(ResearchSource, source_id)

    if not source:
        raise HTTPException(status_code=404, detail="Research source not found")

    return source_dict(source)


@app.put("/research/sources/{source_id}", tags=["research"])
def update_source(
    source_id: int,
    body: ResearchSourceUpdate,
    db: Session = Depends(get_db),
):
    source = db.get(ResearchSource, source_id)

    if not source:
        raise HTTPException(status_code=404, detail="Research source not found")

    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(source, key, value)

    db.commit()
    db.refresh(source)

    return source_dict(source)


@app.delete("/research/sources/{source_id}", tags=["research"])
def delete_source(source_id: int, db: Session = Depends(get_db)):
    source = db.get(ResearchSource, source_id)

    if not source:
        raise HTTPException(status_code=404, detail="Research source not found")

    db.delete(source)
    db.commit()

    return {"message": "Research source deleted", "id": source_id}


# ---------------------------------------------------------------------------
# Goal Evidence
# ---------------------------------------------------------------------------

@app.get("/evidence/goals", tags=["evidence"])
def list_goal_evidence(
    db: Session = Depends(get_db),
    player_id: Optional[int] = None,
    verified: Optional[bool] = None,
):
    query = db.query(GoalEvidence)

    if player_id is not None:
        query = query.filter(GoalEvidence.player_id == player_id)

    if verified is not None:
        query = query.filter(GoalEvidence.verified == verified)

    return [
        evidence_dict(x)
        for x in query.order_by(GoalEvidence.id.desc()).all()
    ]


@app.post("/evidence/goals", tags=["evidence"])
def create_goal_evidence(
    body: GoalEvidenceCreate,
    db: Session = Depends(get_db),
):
    player = db.get(Player, body.player_id)

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    item = GoalEvidence(**body.model_dump())

    db.add(item)
    db.commit()
    db.refresh(item)

    return evidence_dict(item)


@app.get("/evidence/goals/{evidence_id}", tags=["evidence"])
def get_goal_evidence(evidence_id: int, db: Session = Depends(get_db)):
    item = db.get(GoalEvidence, evidence_id)

    if not item:
        raise HTTPException(status_code=404, detail="Goal evidence not found")

    return evidence_dict(item)


@app.put("/evidence/goals/{evidence_id}", tags=["evidence"])
def update_goal_evidence(
    evidence_id: int,
    body: GoalEvidenceUpdate,
    db: Session = Depends(get_db),
):
    item = db.get(GoalEvidence, evidence_id)

    if not item:
        raise HTTPException(status_code=404, detail="Goal evidence not found")

    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return evidence_dict(item)


@app.post("/evidence/goals/{evidence_id}/verify", tags=["evidence"])
def verify_goal_evidence(evidence_id: int, db: Session = Depends(get_db)):
    item = db.get(GoalEvidence, evidence_id)

    if not item:
        raise HTTPException(status_code=404, detail="Goal evidence not found")

    item.verified = True
    db.commit()
    db.refresh(item)

    return evidence_dict(item)


@app.delete("/evidence/goals/{evidence_id}", tags=["evidence"])
def delete_goal_evidence(evidence_id: int, db: Session = Depends(get_db)):
    item = db.get(GoalEvidence, evidence_id)

    if not item:
        raise HTTPException(status_code=404, detail="Goal evidence not found")

    db.delete(item)
    db.commit()

    return {"message": "Goal evidence deleted", "id": evidence_id}


# ---------------------------------------------------------------------------
# Production Projects
# ---------------------------------------------------------------------------

@app.get("/production/projects", tags=["production"])
def list_projects(
    db: Session = Depends(get_db),
    status: Optional[str] = None,
):
    query = db.query(ProductionProject)

    if status:
        query = query.filter(ProductionProject.status == status)

    return [
        project_dict(x)
        for x in query.order_by(ProductionProject.id.desc()).all()
    ]


@app.post("/production/projects", tags=["production"])
def create_project(
    body: ProductionProjectCreate,
    db: Session = Depends(get_db),
):
    if body.story_id is not None and not db.get(Story, body.story_id):
        raise HTTPException(status_code=404, detail="Story not found")

    project = ProductionProject(**body.model_dump())

    db.add(project)
    db.commit()
    db.refresh(project)

    return project_dict(project)


@app.get("/production/projects/{project_id}", tags=["production"])
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.get(ProductionProject, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Production project not found")

    return project_dict(project)


@app.put("/production/projects/{project_id}", tags=["production"])
def update_project(
    project_id: int,
    body: ProductionProjectUpdate,
    db: Session = Depends(get_db),
):
    project = db.get(ProductionProject, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Production project not found")

    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    return project_dict(project)


@app.delete("/production/projects/{project_id}", tags=["production"])
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.get(ProductionProject, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Production project not found")

    db.query(ProductionScene).filter(
        ProductionScene.project_id == project_id
    ).delete(synchronize_session=False)

    db.delete(project)
    db.commit()

    return {"message": "Production project deleted", "id": project_id}


# ---------------------------------------------------------------------------
# Production Scenes
# ---------------------------------------------------------------------------

@app.get("/production/projects/{project_id}/scenes", tags=["production"])
def list_scenes(project_id: int, db: Session = Depends(get_db)):
    if not db.get(ProductionProject, project_id):
        raise HTTPException(status_code=404, detail="Production project not found")

    scenes = db.query(ProductionScene).filter(
        ProductionScene.project_id == project_id
    ).order_by(ProductionScene.scene_number.asc()).all()

    return [scene_dict(x) for x in scenes]


@app.post("/production/projects/{project_id}/scenes", tags=["production"])
def create_scene(
    project_id: int,
    body: ProductionSceneCreate,
    db: Session = Depends(get_db),
):
    if not db.get(ProductionProject, project_id):
        raise HTTPException(status_code=404, detail="Production project not found")

    scene = ProductionScene(
        project_id=project_id,
        **body.model_dump(),
    )

    db.add(scene)
    db.commit()
    db.refresh(scene)

    return scene_dict(scene)


@app.put("/production/scenes/{scene_id}", tags=["production"])
def update_scene(
    scene_id: int,
    body: ProductionSceneUpdate,
    db: Session = Depends(get_db),
):
    scene = db.get(ProductionScene, scene_id)

    if not scene:
        raise HTTPException(status_code=404, detail="Production scene not found")

    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(scene, key, value)

    db.commit()
    db.refresh(scene)

    return scene_dict(scene)


@app.delete("/production/scenes/{scene_id}", tags=["production"])
def delete_scene(scene_id: int, db: Session = Depends(get_db)):
    scene = db.get(ProductionScene, scene_id)

    if not scene:
        raise HTTPException(status_code=404, detail="Production scene not found")

    db.delete(scene)
    db.commit()

    return {"message": "Production scene deleted", "id": scene_id}


# ---------------------------------------------------------------------------
# Dashboard statistics
# ---------------------------------------------------------------------------

@app.get("/dashboard/stats", tags=["dashboard"])
def dashboard_stats(db: Session = Depends(get_db)):
    return {
        "players": db.query(func.count(Player.id)).scalar() or 0,
        "clubs": db.query(func.count(Club.id)).scalar() or 0,
        "stories": db.query(func.count(Story.id)).scalar() or 0,
        "draft_stories": db.query(func.count(Story.id)).filter(
            Story.status == "draft"
        ).scalar() or 0,
        "published_stories": db.query(func.count(Story.id)).filter(
            Story.status == "published"
        ).scalar() or 0,
        "goal_evidence": db.query(func.count(GoalEvidence.id)).scalar() or 0,
        "verified_evidence": db.query(func.count(GoalEvidence.id)).filter(
            GoalEvidence.verified == True
        ).scalar() or 0,
        "research_sources": db.query(func.count(ResearchSource.id)).scalar() or 0,
        "verified_sources": db.query(func.count(ResearchSource.id)).filter(
            ResearchSource.verified == True
        ).scalar() or 0,
        "production_projects": db.query(func.count(ProductionProject.id)).scalar() or 0,
        "production_scenes": db.query(func.count(ProductionScene.id)).scalar() or 0,
    }
