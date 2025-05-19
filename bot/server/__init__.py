import os
import traceback
from contextlib import asynccontextmanager

import aiohttp
from aiogram.types import Update
from fastapi import FastAPI

from bot import bot, dp
from data.logger_config import logger
from server.routes import router_api
from setup import setup_aiogram
from data.config import WEBHOOK_PATH, SERVER_ADDRESS, USE_NGROK, NGROK_INTERFACE_HOST, NGROK_INTERFACE_PORT
from server.routes.mini_app import router as mini_app_router
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request

async def get_ngrok_url() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{NGROK_INTERFACE_HOST}:{NGROK_INTERFACE_PORT}/api/tunnels") as resp:
            data = await resp.json()
    for t in data.get("tunnels", []):
        if t.get("proto") == "https":
            return t["public_url"]
    raise RuntimeError("ngrok HTTPS tunnel not found")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # === startup ===
    await setup_aiogram(dp, bot)

    if USE_NGROK:
        public = await get_ngrok_url()
        webhook_url = f"{public}{WEBHOOK_PATH}"
    else:
        webhook_url = f"{SERVER_ADDRESS}{WEBHOOK_PATH}"

    logger.info("Webhook URL: %s", webhook_url)
    await bot.set_webhook(url=webhook_url, drop_pending_updates=True)
    app.logger = app.logger if hasattr(app, "logger") else None
    yield
    # === shutdown ===
    await bot.delete_webhook()

app = FastAPI(lifespan=lifespan)

app.include_router(mini_app_router, prefix='/miniapp', tags=["Mini App"])
app.include_router(router_api, prefix='/api', tags=["API"])
app.mount("/static", StaticFiles(directory="server/static"), name="static")


@app.get("/")
async def root():
    return {"message": "Welcome to the main server!"}


@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    update = Update(**(await request.json()))
    try:
        await dp.feed_update(bot, update)
    except Exception:
        traceback.print_exc()
    return {"status": "ok"}

