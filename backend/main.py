from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app import models
from app.database import engine
from app.config import SECRET_KEY
from app.routers import users, admin

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Backend API")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.include_router(users.router)
app.include_router(admin.router)
