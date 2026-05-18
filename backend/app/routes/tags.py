from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..database import get_session
from ..helpers import get_or_create_tag
from ..models import Tag

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/")
def list_tags(session: Session = Depends(get_session)):
    return session.exec(select(Tag)).all()


@router.post("/")
def create_tag(name: str, session: Session = Depends(get_session)):
    return get_or_create_tag(name, session)
