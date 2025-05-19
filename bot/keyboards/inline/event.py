from aiogram.filters.callback_data import CallbackData
from .callback import SubActionEventCallback
from .consts import InlineConstructor


def event_details_kb(
        event_url: str,
        event_id: int,
        is_subscription: bool,
        callback_button_back: str = None
):
    actions = [
        {
            "text": "🎟 Купити квиток",
            "url": event_url
        },
        {
            "text": "🔔 Підписатись на подію",
            "callback_data": SubActionEventCallback(
                event_id=event_id,
                type_action="sub",
                by="event",
                additional_values=callback_button_back
            ).wrap()
        } if not is_subscription else {
            "text": "🔕 Відписатись від події",
            "callback_data": SubActionEventCallback(
                event_id=event_id,
                type_action="unsub",
                by="event",
                additional_values=callback_button_back
            ).wrap()
        },
    ]
    schema = [1, 1]

    if callback_button_back:
        actions.append(
            {
                "text": "🔙 Назад",
                "callback_data": callback_button_back
            }
        )
        schema.append(1)

    kb = InlineConstructor.create_kb(
        actions, schema
    )

    return kb