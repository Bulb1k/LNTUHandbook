from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import httpx

from .. import crud, schemas
from ..config import ADMIN_USERNAME, ADMIN_PASSWORD, BOT_API_URL
from ..dependencies import get_db

router = APIRouter(tags=["admin"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def root(_: Request):
    return RedirectResponse("/admin", status_code=status.HTTP_302_FOUND)


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": ""})


@router.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        request.session["auth"] = True
        return RedirectResponse("/admin", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        "login.html", {"request": request, "error": "Невірний логін або пароль"}
    )


@router.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("auth"):
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
    stats = crud.get_stats(db)
    return templates.TemplateResponse("dashboard.html", {"request": request, **stats})


@router.get("/admin/users", response_class=HTMLResponse)
def admin_users(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("auth"):
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
    users = crud.get_users(db)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@router.get("/admin/users/{user_id}/edit", response_class=HTMLResponse)
def edit_user_page(user_id: int, request: Request, db: Session = Depends(get_db)):
    if not request.session.get("auth"):
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse(
        "edit_user.html",
        {"request": request, "user": user, "error": ""},
    )


@router.post("/admin/users/{user_id}/edit", response_class=HTMLResponse)
def edit_user(
    user_id: int,
    request: Request,
    facultative: str = Form(""),
    course: str = Form(""),
    group: str = Form(""),
    db: Session = Depends(get_db),
):
    if not request.session.get("auth"):
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    data = schemas.UserUpdate(
        facultative=facultative or None,
        course=course or None,
        group=group or None,
    )
    crud.update_user(db, chat_id=db_user.chat_id, data=data)
    return RedirectResponse("/admin/users", status_code=status.HTTP_302_FOUND)


@router.post("/admin/users/{user_id}/delete")
def delete_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    if not request.session.get("auth"):
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
    deleted = crud.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return RedirectResponse("/admin/users", status_code=status.HTTP_302_FOUND)


@router.get("/admin/push", response_class=HTMLResponse)
def push_page(request: Request):
    if not request.session.get("auth"):
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        "push.html",
        {
            "request": request,
            "result": None,
            "error": "",
            "message_text": "",
            "chat_ids": "",
            "facultative": "",
            "course": "",
            "group": "",
        },
    )


@router.post("/admin/push", response_class=HTMLResponse)
def send_push(
    request: Request,
    message_text: str = Form(...),
    chat_ids: str = Form(""),
    facultative: str = Form(""),
    course: str = Form(""),
    group: str = Form(""),
    db: Session = Depends(get_db),
):
    if not request.session.get("auth"):
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)

    ids: list[int] = []
    if chat_ids:
        ids = [int(cid.strip()) for cid in chat_ids.split(",") if cid.strip()]
    else:
        ids = crud.get_chat_ids_by_filters(db, facultative or None, course or None, group or None)
        if not ids:
            ids = [u.chat_id for u in crud.get_users(db)]

    payload = {"message_text": message_text}
    if len(ids) == 1:
        payload["chat_id"] = ids[0]
    else:
        payload["chat_ids"] = ids

    try:
        resp = httpx.post(f"{BOT_API_URL}/push_notification", json=payload, timeout=10)
        result = resp.json()
    except Exception as exc:
        result = {"status": "error", "detail": str(exc)}

    return templates.TemplateResponse(
        "push.html",
        {
            "request": request,
            "result": result,
            "error": "",
            "message_text": message_text,
            "chat_ids": chat_ids,
            "facultative": facultative,
            "course": course,
            "group": group,
        },
    )


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
