from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State

from dto import EventDto
from dto.single import BearerTokenDto
from keyboards.inline import build_paginated_keyboard, event_details_kb
from keyboards.inline.callback import EventsCallback, EventDetailsCallback, EventsByDateCallback
from services.http_client import HttpData, HttpUser
from state import CabinetState
from datetime import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext
from bot import bot
from utils.template_engine import render_template
from .helper import independent_message
from texts import texts
from data.config import BASE_DIR
from utils.json_manager import get_json
from utils.format_date import format_ukrainian_date
from .paginated import Pagination



class Event(Pagination):

    @classmethod
    async def show_events(
            cls,
            state: FSMContext,
            venue_id: int = None,
            full_date: str = None,
            city_id: int = None,
            current_page: int = 1,
            custom_state: State = None,
            callback_button_back: str = "main_menu",
            **kwargs
        ):
        """
        format full_date: %Y-%m-%d
        """

        data = await state.get_data()

        response = await HttpData.get_events(EventDto(
            venue_id=venue_id,
            full_date=full_date,
            page=current_page,
        ))

        if response.get('code') != 200:
            return await independent_message(texts.services.SERVICE_ERROR.format(error=response.get('message', '')))
        events = response.get('data', [])
        events = [events[i:i + cls.chunk_size] for i in range(0, len(events), cls.chunk_size)]

        if current_page > len(events) or current_page <= 0:
            return

        if venue_id:
            callback_events = EventsCallback(
                city_id=city_id,
                venue_id=venue_id,
                page=current_page,
            )
        elif full_date:
            events_date = datetime.strptime(full_date, "%Y-%m-%d")
            callback_events = EventsByDateCallback(
                day=events_date.day,
                year=events_date.year,
                month=events_date.month
            )
        else:
            raise TypeError

        button_back = {
            "text": texts.keyboards.BACK,
            "callback_data": callback_button_back
        }

        kb_event_actions = []
        for event in events[current_page - 1]:
            event_date = datetime.strptime(event.get('date'), "%Y-%m-%dT%H:%M:%S.%fZ")
            text = f"{event_date.strftime('%d-%m')} | {event.get('title')} | {'✅' if event.get('has_free_seats') else '❌'}"

            event_btn = {
                "text": text,
                "callback_data": EventDetailsCallback(
                    event_id=event.get('id'),
                    additional_values=callback_events.wrap(),
                ).wrap()
            }
            kb_event_actions.append(event_btn)

        callback_events.additional_values = callback_button_back
        kb = build_paginated_keyboard(
            number_page={'max': len(events), 'current': int(current_page)},
            items=kb_event_actions,
            navigation_callbacks={
                "previous": callback_events.pack_event_by_previous_page(),
                "next": callback_events.pack_event_by_next_page()
            },
            additional_buttons=[button_back]
        )
        
        msg_for_delete = data.get('msg_for_delete', [])
        msgs = await cls.send_message(reply_markup=kb, text=texts.asking.CHOICE_EVENT, **kwargs)
        msg_for_delete.append(msgs)

        if custom_state is not None:
            await state.set_state(custom_state)
        
        await state.update_data(
            events=events[current_page - 1],
            msg_for_delete=msg_for_delete
        )


    @classmethod
    async def show_event_details(
            cls,
            state: FSMContext,
            event_id: int,
            custom_state: State = None,
            callback_button_back: str = "main_menu",
            **kwargs
    ):

        data = await state.get_data()
        event = None
        for event in data.get("events", []):
            if int(event.get('id')) == event_id:
                event = event
                break
        else:
            return

        response = await HttpUser.get_subscribe(bearer_token=BearerTokenDto(data.get('token')))
        if response.get('code') != 200:
            return await independent_message(texts.services.SERVICE_ERROR.format(error=response.get('message', '')))

        events_subscription = response.get('data', [])
        for event_subscription in events_subscription:
            if event_subscription.get('id') == event_id:
                event['is_subscription'] = True
                break
        else:
            event['is_subscription'] = False

        kb = event_details_kb(
            event_url=event.get('concert_event_page'),
            event_id=event_id,
            is_subscription=event['is_subscription'],
            callback_button_back=callback_button_back
        )

        event["date"] = format_ukrainian_date(event.get("date"))
        template = render_template("event_details.js2", event=event)

        msg_for_delete = data.get('msg_for_delete', [])
        msgs = await cls.send_message(reply_markup=kb, text=template, **kwargs)
        msg_for_delete.append(msgs)

        if custom_state is not None:
            await state.set_state(custom_state)

        await state.update_data(
            event_id=event_id,
            msg_for_delete=msg_for_delete
        )



        







