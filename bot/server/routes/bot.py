import re

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from ..schemas import bot as bot_schema
from bot import bot, dp
from utils.template_engine import render_template
import texts
from aiogram.fsm.context import FSMContext, StorageKey

router = APIRouter()


@router.post("/push_notification", response_model=bot_schema.ResponsePushNotification)
async def send_message(request: bot_schema.PushNotification):
    text_html = request.message_text
    success_ids = []

    text_html = re.sub(r'</?p>', '\n\n', text_html)
    text_html = re.sub(r'<br\s*/?>', '\n', text_html)
    for i in range(1, 7):
        text_html = re.sub(fr'<h{i}[^>]*>(.*?)</h{i}>', r'\n<b>\1</b>\n', text_html, flags=re.DOTALL)
    text = re.sub(r'</?(div|span)[^>]*>', '', text_html)

    if request.chat_id:
        await bot.send_message(request.chat_id, text, parse_mode=request.parse_mode)
        success_ids.append(request.chat_id)
    elif request.chat_ids:
        for chat_id in request.chat_ids:
            try:
                await bot.send_message(chat_id, text, parse_mode=request.parse_mode)
                success_ids.append(chat_id)
            except Exception as e:
                pass

    return {"status": "success", "sent_to": success_ids}


