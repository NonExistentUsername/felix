from telegram import tbot
from telegram import BotCommandEvent, BotCallbackEvent
from telebot import types

from core.tools import Observable

command_observable_component = Observable()


@tbot.message_handler(commands=["settings"])
def settings_command(message: types.Message) -> None:
    command_observable_component.notify(
        BotCommandEvent(
            "open_settings",
            chat_id=message.chat.id,
            user_id=message.from_user.id,
        )
    )


@tbot.callback_query_handler(func=lambda call: call.data == "open_language_settings")
def open_language_settings_callback(call: types.CallbackQuery):
    command_observable_component.notify(
        BotCallbackEvent(
            call.data,
            chat_id=call.message.chat.id,
            user_id=call.from_user.id,
            message_id=call.message.id,
        )
    )


@tbot.callback_query_handler(func=lambda call: call.data[:13] == "set_language_")
def set_language_callback(call: types.CallbackQuery):
    command_observable_component.notify(
        BotCommandEvent(
            call.data[:12],
            chat_id=call.message.chat.id,
            user_id=call.from_user.id,
            language_code=call.data[13:],
        )
    )


@tbot.callback_query_handler(func=lambda call: call.data[:13] == "open_settings")
def open_settings_callback(call: types.CallbackQuery):
    command_observable_component.notify(
        BotCallbackEvent(
            call.data,
            chat_id=call.message.chat.id,
            user_id=call.from_user.id,
            message_id=call.message.id,
        )
    )
