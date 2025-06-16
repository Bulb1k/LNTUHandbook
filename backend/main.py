from fastapi import FastAPI, Depends, Request, Form, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
import httpx

from app import models, schemas, crud
from app.database import SessionLocal, engine
from app.config import ADMIN_USERNAME, ADMIN_PASSWORD, SECRET_KEY, BOT_API_URL

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Backend API")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return RedirectResponse("/admin", status_code=status.HTTP_302_FOUND)


@app.get("/users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_telegram(db, telegram_id=user.telegram_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": ""})


@app.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        request.session["auth"] = True
        return RedirectResponse("/admin", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        "login.html", {"request": request, "error": "Invalid credentials"}
    )


@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("auth"):
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
    stats = crud.get_stats(db)
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, **stats}
    )


@app.get("/admin/users", response_class=HTMLResponse)
def admin_users(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("auth"):
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
    users = crud.get_users(db)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/admin/push", response_class=HTMLResponse)
def push_page(request: Request):
    if not request.session.get("auth"):
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("push.html", {"request": request, "result": None, "error": "", "message_text": ""})


@app.post("/admin/push", response_class=HTMLResponse)
def send_push(request: Request, message_text: str = Form(...), chat_ids: str = Form("")):
    if not request.session.get("auth"):
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)

    if not chat_ids:
        return templates.TemplateResponse(
            "push.html",
            {"request": request, "error": "Chat ID(s) required", "result": None, "message_text": message_text},
        )

    ids = [cid.strip() for cid in chat_ids.split(",") if cid.strip()]
    payload = {"message_text": message_text}
    if len(ids) == 1:
        payload["chat_id"] = int(ids[0])
    else:
        payload["chat_ids"] = [int(i) for i in ids]

    try:
        resp = httpx.post(f"{BOT_API_URL}/push_notification", json=payload, timeout=10)
        result = resp.json()
    except Exception as exc:
        result = {"status": "error", "detail": str(exc)}

    return templates.TemplateResponse(
        "push.html",
        {"request": request, "result": result, "error": "", "message_text": message_text},
    )


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
