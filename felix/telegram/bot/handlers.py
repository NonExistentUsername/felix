from telebot import types
from . import tbot

@tbot.message_handler(commands=["start"])
def send_start_message(message: types.Message) -> None:
    tbot.reply_to(message, "Example")

@tbot.message_handler(commands=["/create_pet"])
def create_pet_command(message: types.Message) -> None:
    pass