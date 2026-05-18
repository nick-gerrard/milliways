from fastapi import Depends, HTTPException, Request
from sqlmodel import Session

from .database import get_session
from .models import User


def get_current_user(request: Request, session: Session = Depends(get_session)) -> User:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = session.get(User, user_id)
    if not user:
        request.session.clear()
        raise HTTPException(status_code=401, detail="User not found")
    return user


def get_optional_user(request: Request, session: Session = Depends(get_session)) -> User | None:
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return session.get(User, user_id)
