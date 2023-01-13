from telebot import types
from . import tbot

from ...core.tools import Observable
from .events import BotCommandEvent

command_observable_component = Observable()

@tbot.message_handler(commands=["start"])
def send_start_message(message: types.Message) -> None:
    tbot.reply_to(message, "Example")

@tbot.message_handler(commands=["/create_pet"])
def create_pet_command(message: types.Message) -> None:
    command_observable_component.notify(BotCommandEvent("create_pet", chat_id=message.chat.id))