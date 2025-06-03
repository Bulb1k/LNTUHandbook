import json

from data.config import BASE_DIR


def get_json(file_name: str) -> dict:
    with open(f'{BASE_DIR}/{file_name}', mode='r') as file:
        data = file.read()

        return json.loads(data)