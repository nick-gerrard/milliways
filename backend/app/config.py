from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

_default_db = Path(__file__).resolve().parent.parent / "milliways.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{_default_db}")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
SESSION_SECRET = os.getenv("SESSION_CLIENT_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
CALLBACK_URL = os.getenv("CALLBACK_URL", "http://localhost:8000/auth/callback")
