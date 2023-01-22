from telegram import tbot
from telegram import BotCommandEvent
from telebot import types

from core.tools import Observable

command_observable_component = Observable()


@tbot.message_handler(commands=["create_pet"])
def create_pet_command(message: types.Message) -> None:
    command_observable_component.notify(
        BotCommandEvent(
            "create_pet", chat_id=message.chat.id, user_id=message.from_user.id
        )
    )


@tbot.message_handler(
    func=lambda message: str(message.text).startswith("/set_pet_name")
)
def set_pet_name_command(message: types.Message) -> None:
    command_observable_component.notify(
        BotCommandEvent(
            "set_pet_name",
            chat_id=message.chat.id,
            new_name=str(message.text)[14:],
            user_id=message.from_user.id,
        )
    )


@tbot.message_handler(commands=["pet"])
def get_pet_command(message: types.Message) -> None:
    command_observable_component.notify(
        BotCommandEvent(
            "get_pet",
            chat_id=message.chat.id,
            user_id=message.from_user.id,
        )
    )
