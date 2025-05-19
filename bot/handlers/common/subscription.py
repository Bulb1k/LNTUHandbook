from typing import Optional

from aiogram.fsm.state import State
from aiogram import types
from aiogram.fsm.context import FSMContext
from pydantic.v1.errors import cls_kwargs

from bot import bot
from data.logger_config import logger
from handlers.common.helper import independent_message
from handlers.common.paginated import Pagination
from keyboards.inline import build_paginated_keyboard, build_subscription_paginated_keyboard
from keyboards.inline.callback import SubEventDetailsCallback, SubCityCallback, VenuesCallback
from state import CabinetState
from texts import texts
from services.http_client import HttpUser
from dto.single import BearerTokenDto, EventIdDto, CityIdDto


class Subscription(Pagination):
    @classmethod
    async def _dont_have_sub(cls, type_sub: str, state: FSMContext, **kwargs):
        if type_sub == "events":
            if kwargs.get('callback'):
                callback: types.CallbackQuery = kwargs.get('callback')
                await callback.answer(text=texts.asking.YOU, show_alert=True)
            else:
                await independent_message(msg_text=texts.asking.YOU_DONT_HAVE_SUBSCRIPTION_EVENT, **kwargs)
            return cls.show_subscriptions(
                state=state,
                type_sub="cities",
            )
        elif type_sub == "cities":
            if kwargs.get('callback'):
                callback: types.CallbackQuery = kwargs.get('callback')
                await callback.answer(text=texts.asking.YOU_DONT_HAVE_SUBSCRIPTION_EVENT, show_alert=True)
            else:
                await independent_message(msg_text=texts.asking.YOU_DONT_HAVE_SUBSCRIPTION_EVENT, **kwargs)
            return cls.show_subscriptions(
                state=state,
                type_sub="events",
            )

    @classmethod
    async def show_subscriptions(
            cls,
            state: FSMContext,
            current_page: int = 1,
            type_sub: str = "events",
            custom_state: State = None,
            **kwargs
    ):
        data = await state.get_data()

        if type_sub == "events":
            response = await HttpUser.get_subscribe(page=current_page, bearer_token=BearerTokenDto(data.get('token')))
        elif type_sub == "cities":
            response = await HttpUser.get_city_subscribe(page=current_page, bearer_token=BearerTokenDto(data.get('token')))
        else:
            raise NotImplementedError

        if response.get('code') != 200:
            return await independent_message(texts.services.SERVICE_ERROR.format(error=response.get('message', '')))
        subscriptions = response.get('data', [])
        pagination = response.get('pagination')

        # if len(subscriptions) <= 0:
        #     return cls._dont_have_sub(type_sub, state, **kwargs)
        if current_page > pagination['last_page'] or current_page <= 0:
            return

        button_back = {"text": texts.keyboards.CLOSE, "callback_data": "close_sub"}
        if kwargs.get('button_back'):
            button_back = kwargs.get('button_back')

        kb_subscribe_event_actions = []
        for subscription in subscriptions:
            if type_sub == "cities":
                callback_data = VenuesCallback(
                    city_id=subscription.get('id'),
                )
                text = subscription.get("name")
            elif type_sub == "events":
                callback_data = SubEventDetailsCallback(
                    event_id=subscription.get('id'),
                )
                text = subscription.get("title")
            else:
                raise NotImplementedError

            kb_subscribe_event_actions.append(
                {
                    "text": text,
                    "callback_data": callback_data
                }
            )

        kb = build_subscription_paginated_keyboard(
            number_page={'max': pagination.get('last_page'), 'current': int(current_page)},
            actions=kb_subscribe_event_actions,
            type_sub=type_sub,
            additional_buttons=[button_back]
        )

        msg_for_delete = data.get('msg_for_delete', [])
        msgs = await cls.send_message(reply_markup=kb, text=texts.asking.DETAIL_SUBSCRIPTION, **kwargs)
        msg_for_delete.append(msgs)

        if custom_state is not None:
            await state.set_state(custom_state)

        await state.update_data(
            events=subscriptions if type_sub == "events" else None,
            msg_for_delete=msg_for_delete
        )

    @staticmethod
    async def actions_subscription_event(type_action: str, event_id: int, state: FSMContext, callback: types.CallbackQuery):
        data = await state.get_data()

        if type_action == 'unsub':
            responses = await HttpUser.unsubscribe(
                EventIdDto(event_id=event_id),
                BearerTokenDto(token=data.get('token'))
            )
            if responses.get('code') != 200:
                return await independent_message(
                    texts.services.SERVICE_ERROR.format(error=responses.get('message', '')),
                    chat_id=callback.from_user.id
                )
            await callback.answer(texts.asking.YOU_UNSUBSCRIBED_EVENT, show_alert=True)
        elif type_action == 'sub':
            responses = await HttpUser.subscribe(
                EventIdDto(event_id=event_id),
                BearerTokenDto(token=data.get('token'))
            )

            if responses.get('code') != 200:
                return await independent_message(
                    texts.services.SERVICE_ERROR.format(error=responses.get('message', '')),
                    chat_id=callback.from_user.id
                )
            await callback.answer(texts.asking.YOU_SUBSCRIBED_EVENT, show_alert=True)


    @staticmethod
    async def actions_subscription_city(type_action: str, city_id: int, state: FSMContext, callback: types.CallbackQuery):
        data = await state.get_data()

        if type_action == 'unsub':
            responses = await HttpUser.unsubscribe_city(
                CityIdDto(city_id=city_id),
                BearerTokenDto(token=data.get('token'))
            )
            if responses.get('code') != 200:
                return await independent_message(
                    texts.services.SERVICE_ERROR.format(error=responses.get('message', '')),
                    chat_id=callback.from_user.id
                )
            await callback.answer(texts.asking.YOU_UNSUBSCRIBED_CITY, show_alert=True)

        elif type_action == 'sub':
            responses = await HttpUser.subscribe_city(
                CityIdDto(city_id=city_id),
                BearerTokenDto(token=data.get('token'))
            )

            if responses.get('code') != 200:
                return await independent_message(
                    texts.services.SERVICE_ERROR.format(error=responses.get('message', '')),
                    chat_id=callback.from_user.id
                )
            await callback.answer(texts.asking.YOU_SUBSCRIBED_CITY, show_alert=True)

