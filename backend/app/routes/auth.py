from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from ..config import FRONTEND_URL, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from ..database import get_session
from ..deps import get_current_user
from ..models import User

oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/google")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request, session: Session = Depends(get_session)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to retrieve user info from Google")

    user = session.exec(select(User).where(User.google_id == user_info["sub"])).first()
    if not user:
        user = User(
            google_id=user_info["sub"],
            email=user_info["email"],
            name=user_info["name"],
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    request.session["user_id"] = user.id
    return RedirectResponse(url=FRONTEND_URL)


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout", status_code=204)
def logout(request: Request):
    request.session.clear()
