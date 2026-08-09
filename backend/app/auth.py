import os
import logging
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .database import SessionLocal, User

logger = logging.getLogger(__name__)

JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)
bearer_scheme = HTTPBearer(auto_error=False)


# ---------------------------------------------------------------------------
# Password helpers
# ---------------------------------------------------------------------------

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain[:72])


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain[:72], hashed)


# ---------------------------------------------------------------------------
# Token helpers
# ---------------------------------------------------------------------------

def create_access_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)


def decode_token(token: str) -> str:
    """Return email from token or raise HTTPException."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# ---------------------------------------------------------------------------
# FastAPI dependency — optional auth (returns user or None)
# ---------------------------------------------------------------------------

def get_optional_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    if not credentials:
        return None
    email = decode_token(credentials.credentials)
    user = get_user_by_email(db, email)
    return user


# ---------------------------------------------------------------------------
# FastAPI dependency — required auth
# ---------------------------------------------------------------------------

def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    email = decode_token(credentials.credentials)
    user = get_user_by_email(db, email)
    if not user or not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return user


# ---------------------------------------------------------------------------
# Seed admin on first run
# ---------------------------------------------------------------------------

def ensure_admin_exists(db: Session):
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_email or not admin_password:
        logger.warning(
            "ADMIN_EMAIL or ADMIN_PASSWORD not set — skipping admin seed."
        )
        return

    existing = get_user_by_email(db, admin_email)
    if not existing:
        user = User(
            email=admin_email,
            hashed_password=hash_password(admin_password),
            is_admin=True,
        )
        db.add(user)
        db.commit()
        logger.info("Admin user created: %s", admin_email)
    else:
        logger.info("Admin user already exists: %s", admin_email)
