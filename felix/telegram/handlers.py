from telebot import types
from . import tbot

from core.tools import Observable
from .events import BotCommandEvent, BotCallbackEvent
from .messages import txt

command_observable_component = Observable()


@tbot.message_handler(commands=["start"])
def send_start_message(message: types.Message) -> None:
    command_observable_component.notify(
        BotCommandEvent("start", chat_id=message.chat.id)
    )


@tbot.message_handler(commands=["create_pet"])
def create_pet_command(message: types.Message) -> None:
    command_observable_component.notify(
        BotCommandEvent("create_pet", chat_id=message.chat.id)
    )


@tbot.message_handler(commands=["settings"])
def settings_command(message: types.Message) -> None:
    command_observable_component.notify(
        BotCommandEvent("settings", chat_id=message.chat.id)
    )


@tbot.callback_query_handler(func=lambda call: call.data == "open_language_settings")
def open_language_settings_callback(call: types.CallbackQuery):
    command_observable_component.notify(
        BotCallbackEvent(
            "open_language_settings",
            chat_id=call.message.chat.id,
            message_id=call.message.id,
        )
    )


@tbot.callback_query_handler(func=lambda call: call.data[:13] == "set_language_")
def set_language_callback(call: types.CallbackQuery):
    command_observable_component.notify(
        BotCommandEvent(
            call.data[:12], chat_id=call.message.chat.id, language_code=call.data[13:]
        )
    )


@tbot.callback_query_handler(func=lambda call: call.data[:13] == "open_settings")
def open_settings_callback(call: types.CallbackQuery):
    command_observable_component.notify(
        BotCallbackEvent(
            call.data,
            chat_id=call.message.chat.id,
            message_id=call.message.id,
        )
    )


@tbot.message_handler(commands=["set_pet_name"])
def set_pet_name_command(message: types.Message) -> None:
    command_observable_component.notify(
        BotCommandEvent(
            "set_pet_name", chat_id=message.chat.id, new_name=str(message.text)[13:]
        )
    )


@tbot.message_handler(commands=["pet"])
def get_pet_command(message: types.Message) -> None:
    command_observable_component.notify(
        BotCommandEvent("get_pet", chat_id=message.chat.id)
    )
