from fastapi import FastAPI, Depends
from sqlmodel import Session, select 
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from .database import get_session
from .models import Recipe

from .config import FRONTEND_URL, SESSION_SECRET

app = FastAPI(title="Milliways API")

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/recipes")
def get_recipes(session: Session = Depends(get_session)):
    return session.exec(select(Recipe)).all()
