from fastapi import APIRouter
from .mini_app import router as router_mini_app
from .bot import router as router_bot

router_api = APIRouter()

router_api.include_router(router_bot, tags=["Bot"])