from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram import types
from pydantic.v1.errors import cls_kwargs

from handlers.common.helper import independent_message
from handlers.common.paginated import Pagination, PaginationCallback
from keyboards.inline import choice_city_keyboard, build_paginated_keyboard
from keyboards.inline.callback import CitiesCallback, VenuesCallback
from services.http_client import HttpData, HttpUser
from state import StartState
from texts import texts
from dto import single_dto


class City(Pagination):
    @classmethod
    async def show_cities(cls,
            state: FSMContext,
            current_page: int = 1,
            custom_state: State = None,
            **kwargs
        ):
        data = await state.get_data()

        response = await HttpData.get_city(page=current_page)
        if response.get('code') != 200:
            return await independent_message(texts.services.SERVICE_ERROR.format(error=response.get('message', '')), **kwargs)
        cities = response.get('data', [])
        pagination = response.get('pagination')

        if current_page > pagination['current_page'] or current_page <= 0:
            return

        callback_cities = CitiesCallback(
            page=current_page,
        )

        kb_cities_actions = [
            {
                "text": city.get('name'),
                "callback_data": VenuesCallback(
                    city_id=city.get('id'),
                    additional_values=callback_cities.wrap()
                ).wrap()
            } for city in cities
        ]

        kb = build_paginated_keyboard(
            number_page={'max': pagination['last_page'], 'current': int(current_page)},
            items=kb_cities_actions,
            navigation_callbacks={
                "previous": callback_cities.pack_event_by_previous_page(),
                "next": callback_cities.pack_event_by_next_page()
            },
            additional_buttons=[{"text": texts.keyboards.CLOSE, "callback_data": "close_choice_city"}]

        )

        msg_for_delete = data.get('msg_for_delete', [])
        msgs = await cls.send_message(reply_markup=kb, text=texts.asking.CHOICE_CITY, **kwargs)
        msg_for_delete.append(msgs)

        if custom_state is not None:
            await state.set_state(custom_state)

        await state.update_data(
            cities=cities,
            msg_for_delete=msg_for_delete
        )


    @staticmethod
    async def save_city(callback: types.CallbackQuery, state: FSMContext):
        city_id = int(callback.data.split('_')[-1])
        data = await state.get_data()

        for city in data.get('city_list', []):
            if city.get('id') == city_id:
                await state.update_data(city=city)
                break

        await HttpUser.update(
            single_dto.CityIdDto(city_id),
            single_dto.BearerTokenDto(token=data.get('token'))
        )

        await callback.message.delete()

