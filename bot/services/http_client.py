import copy
import mimetypes
import os

import aiohttp
from data.config import API_BACKEND_URL, API_BACKEND_KEY
from data.logger_config import logger
from dto.abstract_dto import AbstractDto
import json
from dto import single_dto
import dto

class FormDataAdapter:
    @staticmethod
    def adapt(data: dict) -> aiohttp.FormData:
        form = aiohttp.FormData()

        def _add_recursive(prefix, value):
            if isinstance(value, dict):
                for k, v in value.items():
                    new_key = f"{prefix}[{k}]" if prefix else k
                    _add_recursive(new_key, v)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    new_key = f"{prefix}[{i}]"
                    _add_recursive(new_key, item)
            elif isinstance(value, tuple) and len(value) == 3:
                file_obj, filename, content_type = value
                form.add_field(prefix, file_obj, filename=filename, content_type=content_type)
            else:
                form.add_field(prefix, str(value))

        for key, value in data.items():
            _add_recursive(key, value)

        return form


class HttpClient:

    @classmethod
    async def make_request(cls, method: str, path: str, data=None, headers=None, **kwargs):
        headers = headers or {}
        headers["Accept"] = "application/json"

        url = f"{API_BACKEND_URL}{path}"

        if data is not None:
            data = data.to_payload()
        elif data is None and method == "POST":
            raise NotImplementedError

        is_form_data = kwargs.pop("is_form_data", False)
        if is_form_data and data:
            data = cls._prepare_files(data)
            body = FormDataAdapter.adapt(data)
        else:
            body = json.dumps(data) if data else None
            headers["Content-Type"] = "application/json"

        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, data=body, headers=headers, **kwargs) as resp:
                try:
                    response_data = await resp.json()
                except:
                    response_data = await resp.text()

                logger.info(f'REQUEST\nBODY: {body}\nHEADERS: {headers}\nURL: {url}\nRESPONSE: {response_data}')
                return {**response_data, "code": resp.status}

    @staticmethod
    def _prepare_files(data: dict) -> dict:
        if not data:
            return {}

        result = copy.deepcopy(data)

        def _process(obj):
            if isinstance(obj, dict):
                return {k: _process(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [_process(item) for item in obj]
            elif isinstance(obj, str) and os.path.isfile(obj):
                filename = os.path.basename(obj)
                content_type = mimetypes.guess_type(obj)[0] or "application/octet-stream"
                return (open(obj, "rb"), filename, content_type)
            return obj

        return _process(result)


class HttpUser(HttpClient):
    base_url = '/user'

    @classmethod
    async def request(cls, path: str, method: str, data: AbstractDto = None, headers: dict = None, **kwargs) -> dict:
        path = f'{cls.base_url}{path}'
        return await HttpClient.make_request(path=path, method=method, data=data, headers=headers, **kwargs)

    @classmethod
    async def login(cls, data: dto.LoginDto):
        return await cls.request(path='/login', method='POST', data=data)

    @classmethod
    async def get_profile(cls, bearer_token: single_dto.BearerTokenDto):
        return await cls.request(path='/profile', method='GET', headers=bearer_token.to_payload())

    @classmethod
    async def update(cls, data: single_dto.CityIdDto, bearer_token: single_dto.BearerTokenDto):
        return await cls.request(path='/update', method='POST', data=data, headers=bearer_token.to_payload())

    @classmethod
    async def get_subscribe(cls, bearer_token: single_dto.BearerTokenDto, page=1):
        return await cls.request(path=f'/get_subscribe?page={page}', method='GET', headers=bearer_token.to_payload())

    @classmethod
    async def get_city_subscribe(cls, bearer_token: single_dto.BearerTokenDto, page=1):
        return await cls.request(path=f'/get_city_subscribe?page={page}', method='GET', headers=bearer_token.to_payload())

    @classmethod
    async def subscribe(cls, data: single_dto.EventIdDto, bearer_token: single_dto.BearerTokenDto):
        return await cls.request(path='/subscribe', method='POST', data=data, headers=bearer_token.to_payload())

    @classmethod
    async def unsubscribe(cls, data: single_dto.EventIdDto, bearer_token: single_dto.BearerTokenDto):
        return await cls.request(path='/un_subscribe', method='DELETE', data=data, headers=bearer_token.to_payload())

    @classmethod
    async def subscribe_city(cls, data: single_dto.CityIdDto, bearer_token: single_dto.BearerTokenDto):
        return await cls.request(path='/subscribe_city', method='POST', data=data, headers=bearer_token.to_payload())

    @classmethod
    async def unsubscribe_city(cls, data: single_dto.CityIdDto, bearer_token: single_dto.BearerTokenDto):
        return await cls.request(path='/city_un_subscribe', method='DELETE', data=data, headers=bearer_token.to_payload())\

    @classmethod
    async def feed_back(cls, data: single_dto.MessageDto, bearer_token: single_dto.BearerTokenDto):
        return await cls.request(path='/feed_back', method='POST', data=data, headers=bearer_token.to_payload())

class HttpData(HttpClient):
    base_url = '/data'

    @classmethod
    async def request(cls, path: str, method: str, data: AbstractDto = None, headers: dict = None, **kwargs) -> dict:
        path = f'{cls.base_url}{path}'
        return await HttpClient.make_request(path=path, method=method, data=data, headers=headers, **kwargs)

    @classmethod
    async def get_city(cls, page: int = 1):
        return await cls.request(path=f'/get_city?page={page}', method='GET')

    @classmethod
    async def get_venues(cls, data: dto.VenuesDto):
        return await cls.request(path='/get_venues', method='POST', data=data)

    @classmethod
    async def get_events(cls, data: dto.EventDto):
        return await cls.request(path='/get_event', method='POST', data=data)






