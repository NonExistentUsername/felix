from telebot import types
from . import tbot

@tbot.message_handler(commands=["start"])
def send_start_message(message: types.Message) -> None:
    pass