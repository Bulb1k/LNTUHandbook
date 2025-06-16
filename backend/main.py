from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from app import models, schemas, crud
from app.database import SessionLocal, engine
from app.config import ADMIN_SECRET

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Backend API")

templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_telegram(db, telegram_id=user.telegram_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)


@app.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request, secret: str, db: Session = Depends(get_db)):
    if secret != ADMIN_SECRET:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid secret")
    users = crud.get_users(db)
    return templates.TemplateResponse("admin.html", {"request": request, "users": users})
