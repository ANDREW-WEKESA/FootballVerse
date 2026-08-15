import os
import sys
from dotenv import load_dotenv

load_dotenv()

_REQUIRED = ["DATABASE_URL", "JWT_SECRET", "ADMIN_EMAIL", "ADMIN_PASSWORD"]

_missing = [k for k in _REQUIRED if not os.getenv(k)]
if _missing:
    for key in _missing:
        print(f"ERROR: Required environment variable '{key}' is not set.", flush=True)
    sys.exit(1)

DATABASE_URL: str = os.environ["DATABASE_URL"]
JWT_SECRET: str = os.environ["JWT_SECRET"]
ADMIN_EMAIL: str = os.environ["ADMIN_EMAIL"]
ADMIN_PASSWORD: str = os.environ["ADMIN_PASSWORD"]
FOOTBALL_DATA_API_KEY: str = os.getenv("FOOTBALL_DATA_API_KEY", "")

JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24
