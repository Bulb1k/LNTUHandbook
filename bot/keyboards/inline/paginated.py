from typing import Optional, List, Dict, Any
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


