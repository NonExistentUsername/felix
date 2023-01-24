from core.tools import Observable
from telebot import types
from telegram import BotCommandEvent, tbot

command_observable_component = Observable()


@tbot.message_handler(commands=["balance"])
def balance_command(message: types.Message):
    command_observable_component.notify(
        BotCommandEvent(
            "show_balance",
            chat_id=message.chat.id,
            user_id=message.from_user.id,
        )
    )


@tbot.message_handler(commands=["collect_bonus"])
def collect_bonus_command(message: types.Message):
    command_observable_component.notify(
        BotCommandEvent(
            "collect_bonus",
            chat_id=message.chat.id,
            user_id=message.from_user.id,
        )
    )
