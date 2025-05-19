from sys import prefix

from aiogram import types, MagicFilter
from typing import Optional, Type

from aiogram.filters.callback_data import CallbackData, T, CallbackQueryFilter

from handlers.common.helper import independent_message


class Pagination:
    chunk_size = 7

    @staticmethod
    async def send_message(reply_markup: Optional, text: str, **kwargs):
        msg_for_delete = []
        if kwargs.get('message'):
            message: types.Message = kwargs.get('message')
            msg_for_delete.append(message.message_id)
            try:
                await message.edit_text(
                    text=text,
                    reply_markup=reply_markup
                )
            except Exception as e:
                if "message is not modified" in str(e):
                    pass
                else:
                    message = await message.answer(
                        text=text,
                        reply_markup=reply_markup
                    )
                    msg_for_delete.append(message.message_id)

        else:
            message = await independent_message(msg_text=text, reply_markup=reply_markup, **kwargs)
            msg_for_delete.append(message.message_id)

        return msg_for_delete

class PaginationCallback(CallbackData, prefix="pagination"):
    page: int = 1
    additional_values: str | None = None

    def pack_event_by_next_page(self):
        return self.copy(update={"page": self.page + 1}).wrap()

    def pack_event_by_previous_page(self):
        return self.copy(update={"page": self.page - 1}).wrap()

    def wrap(self) -> str:
        additional_values = self.additional_values
        self.additional_values = None
        pack_callback = self.pack()
        pack_callback += "&" + additional_values if additional_values is not None else ''

        return pack_callback

    @classmethod
    def unwrap(cls: Type[T], value: str) -> T:
        if "&" in value:
            additional_values = value.split("&")[-1]
            callback_data = value.split("&")[0]

            callback_data = cls.unpack(callback_data)
            callback_data.additional_values = additional_values

            return callback_data
        return cls.unpack(value)