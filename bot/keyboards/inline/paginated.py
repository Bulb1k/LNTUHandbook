from typing import Optional, List, Dict, Any

from keyboards.inline.callback import (
    SubEventDetailsCallback,
    SubCityCallback, SubList, SubActionCityCallback, SubActionEventCallback
)
from keyboards.inline.consts import InlineConstructor

def build_paginated_keyboard(
    number_page: Dict[str, int],
    items: List[Dict],
    additional_buttons: List[Dict] = None,
    navigation_callbacks: Dict[str, str] = None
    ):

    actions = [
        *items,
    ]
    schema = [1 for _ in range(len(items))]

    if number_page['max'] > 1:
        navigation_actions = [
            {
                "text": "◀️",
                "callback_data": f"{navigation_callbacks['previous']}"
            },
            {
                "text": f"[{number_page['current']}/{number_page['max']}]",
                "callback_data": f"number_page_{number_page['current']}"
            },
            {
                "text": "▶️",
                "callback_data": f"{navigation_callbacks['next']}"
            }
        ]
        for action in navigation_actions:
            actions.append(action)

        schema.append(3)

    if additional_buttons is not None:
        for action in additional_buttons:
            actions.append(action)
        for _ in range(len(additional_buttons)):
            schema.append(1)

    kb = InlineConstructor.create_kb(
        actions=actions, schema=schema)

    return kb


def build_subscription_paginated_keyboard(
            number_page: Dict[str, int],
            actions: List[Dict[str, SubEventDetailsCallback | SubCityCallback]],
            type_sub: str,
            additional_buttons: List[Dict] = None
    ):
    sub_list_callback = SubList(page=number_page['current'], type_sub=type_sub)

    updated_actions = []
    schema = []
    for action in actions:
        callback = action.get('callback_data')


        if type_sub == "events":
            action_unsub = {
                "text": "🔕",
                "callback_data": SubActionEventCallback(
                    event_id=callback.event_id,
                    type_action="unsub",
                    additional_values=SubList(page=number_page['current'], type_sub="events").wrap()
                ).wrap()
            }
        elif type_sub == "cities":
            action_unsub = {
                "text": "🔕",
                "callback_data": SubActionCityCallback(
                    city_id=callback.city_id,
                    type_action="unsub",
                    additional_values=SubList(page=number_page['current'], type_sub="cities").wrap()
                ).wrap()
            }
        else:
            raise NotImplementedError

        updated_actions.append(action)
        updated_actions.append(action_unsub)
        schema.append(2)

    change_type_sub = [
        {
            "text": "✅ Події" if type_sub == "events" else "Події",
            "callback_data": SubList(page=number_page['current'], type_sub="events")
        },
        {
            "text": "✅ Міста" if type_sub == "cities" else "Міста",
            "callback_data": SubList(page=number_page['current'], type_sub="cities")
        }
    ]
    for action in change_type_sub:
        updated_actions.append(action)
    schema.append(2)

    if number_page['max'] > 1:

        navigation_actions = [
            {
                "text": "◀️",
                "callback_data": sub_list_callback.pack_event_by_previous_page()
            },
            {
                "text": f"[{number_page['current']}/{number_page['max']}]",
                "callback_data": f"number_page_{number_page['current']}"
            },
            {
                "text": "▶️",
                "callback_data": sub_list_callback.pack_event_by_next_page()
            }
        ]
        for action in navigation_actions:
            updated_actions.append(action)

        schema.append(3)

    if additional_buttons is not None:
        for action in additional_buttons:
            updated_actions.append(action)
        for _ in range(len(additional_buttons)):
            schema.append(1)
    for action in updated_actions:
        print(action)
    kb = InlineConstructor.create_kb(
        actions=updated_actions, schema=schema)

    return kb



