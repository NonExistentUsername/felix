from telegram import tbot
from telegram import BotCommandEvent
from telebot import types

from core.tools import Observable

command_observable_component = Observable()


@tbot.message_handler(commands=["start"])
def send_start_message(message: types.Message) -> None:
    command_observable_component.notify(
        BotCommandEvent("start", message.chat.id, message.from_user.id)
    )
