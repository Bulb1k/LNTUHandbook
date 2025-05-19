import json
from typing import List, Optional

import aiofiles
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State

from dto.single import BearerTokenDto
from keyboards.inline import build_paginated_keyboard
from keyboards.inline.callback import VenuesCallback, EventsCallback, SubActionCityCallback
from state import CabinetState

from aiogram import types
from aiogram.fsm.context import FSMContext
from bot import bot
from .event import Event
from .helper import independent_message
from texts import texts
from dto import VenuesDto
from services.http_client import HttpData, HttpUser
from .paginated import Pagination


class Venue(Pagination):
    @classmethod
    async def show_venues(
            cls,
            state: FSMContext,
            current_page: int = 1,
            city_id: Optional[int] = None,
            custom_state: State = None,
            callback_button_back: str = 'main_menu',
            **kwargs
        ):

        data = await state.get_data()

        response = await HttpData.get_venues(VenuesDto(
            city_id=city_id if city_id is None else 1,
            has_event=True,
            page=current_page,
        ))
        if response.get('code') != 200:
            return await independent_message(texts.services.SERVICE_ERROR.format(error=response.get('message', '')))
        venues = response.get('data', [])
        pagination = response.get('pagination')

        if current_page > pagination['last_page'] or current_page <= 0:
            return

        callback_venues = VenuesCallback(
            city_id=city_id if city_id is None else 1),
            page=current_page,
        )

        kb_venues_actions = []
        for venue in venues:
            kb_venues_actions.append(
                {"text": venue.get("title"), "callback_data": EventsCallback(
                    venue_id=venue.get("id"),
                    city_id=city_id,
                    additional_values=callback_venues.wrap()
                ).wrap()},
            )

        callback_venues.additional_values = callback_button_back

        response = await HttpUser.get_city_subscribe(BearerTokenDto(data.get('token')))
        subscriptions_city = response.get('data', [])
        is_subscriptions_city = False
        for city in subscriptions_city:
            if int(city.get('id')) == city_id:
                is_subscriptions_city = True
                break

        kb = build_paginated_keyboard(
            number_page={'max': pagination['last_page'], 'current': int(current_page)},
            items=kb_venues_actions,
            navigation_callbacks={
                "previous": callback_venues.pack_event_by_previous_page(),
                "next": callback_venues.pack_event_by_next_page()
            },
            additional_buttons=[
                {
                    "text": "Відписатись від міста 🔕" if is_subscriptions_city else "Підписатись на місто 🔔",
                    "callback_data": SubActionCityCallback(
                        city_id=city_id,
                        by="venues",
                        type_action="unsub" if is_subscriptions_city else "sub",
                        additional_values=callback_button_back
                    ).wrap()
                },
                {"text": texts.keyboards.BACK, "callback_data": callback_button_back}
            ]

        )
        print(kb)

        msg_for_delete = data.get('msg_for_delete', [])
        msgs = await cls.send_message(reply_markup=kb, text=texts.asking.CHOICE_VENUE, **kwargs)
        msg_for_delete.append(msgs)

        if custom_state is not None:
            await state.set_state(custom_state)

        await state.update_data(
            venues=venues,
            msg_for_delete=msg_for_delete
        )









