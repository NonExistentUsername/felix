from telebot import types
from . import tbot

from core.tools import Observable
from .events import BotCommandEvent
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
