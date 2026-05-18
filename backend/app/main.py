from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from .database import get_session
from .models import Recipe, RecipeIngredient, User
from .schemas import RecipeDetail
from .config import FRONTEND_URL, SESSION_SECRET, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from .deps import get_current_user

app = FastAPI(title="Milliways API")

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/auth/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/auth/callback")
async def auth_callback(request: Request, session: Session = Depends(get_session)):
    token = await oauth.google.authorize_access_token(request)
    userinfo = token["userinfo"]

    user = session.exec(select(User).where(User.google_id == userinfo["sub"])).first()
    if not user:
        user = User(
            google_id=userinfo["sub"],
            email=userinfo["email"],
            name=userinfo["name"],
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    request.session["user_id"] = user.id
    return RedirectResponse(url=f"{FRONTEND_URL}/recipes")


@app.get("/auth/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url=f"{FRONTEND_URL}/")


@app.get("/auth/me")
def me(request: Request, session: Session = Depends(get_session)):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return session.get(User, user_id)


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
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe
