from .consts import InlineConstructor

def choice_city_keyboard(city_list: list[dict]):
    actions = [
        {
            "text": city.get('name'),
            "callback_data": f"city_{city.get('id')}"
        }
        for city in city_list
    ]

    schema = [1 for _ in range(len(city_list))]

    kb = InlineConstructor.create_kb(
        actions=actions, schema=schema)

    return kb