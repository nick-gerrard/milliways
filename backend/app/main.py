from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from .database import get_session
from .models import Recipe, RecipeIngredient
from .schemas import RecipeDetail
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


@app.get("/recipes/{recipe_id}", response_model=RecipeDetail)
def get_recipe_details(recipe_id: int, session: Session = Depends(get_session)):
    statement = (
        select(Recipe)
        .where(Recipe.id == recipe_id)
        .options(
            selectinload(Recipe.steps),
            selectinload(Recipe.tags),
            selectinload(Recipe.ingredients).selectinload(RecipeIngredient.ingredient),
        )
    )
    recipe = session.execute(statement).scalar_one_or_none()
    return recipe
