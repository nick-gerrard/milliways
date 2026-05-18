from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from .config import FRONTEND_URL, SESSION_SECRET
from .routes import auth, recipes, shopping, tags

app = FastAPI(title="Milliways API")

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recipes.router)
app.include_router(tags.router)
app.include_router(shopping.router)
app.include_router(auth.router)


@app.get("/health")
def health():
    return {"status": "ok"}
