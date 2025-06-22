from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@router.get("/{chat_id}", response_model=schemas.User)
def read_user(chat_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_chat(db, chat_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_chat(db, chat_id=user.chat_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)


@router.put("/{chat_id}", response_model=schemas.User)
def update_user(chat_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, chat_id=chat_id, data=user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
