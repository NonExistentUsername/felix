from core.tools import Observable
from telebot import types
from telegram import BotCommandEvent, tbot

command_observable_component = Observable()


@tbot.message_handler(commands=["create_pet"])
def create_pet_command(message: types.Message) -> None:
    command_observable_component.notify(
        BotCommandEvent(
            "create_pet", chat_id=message.chat.id, user_id=message.from_user.id
        )
    )


@tbot.message_handler(commands=["delete_pet"])
def delete_pet_command(message: types.Message) -> None:
    command_observable_component.notify(
        BotCommandEvent(
            "delete_pet", chat_id=message.chat.id, user_id=message.from_user.id
        )
    )


@tbot.message_handler(commands=["set_pet_name"])
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
