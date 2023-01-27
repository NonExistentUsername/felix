import os
import typing as t

from core.engine_components.pet_component import IPetEngineComponent
from core.engine_components.telegram_components.chat_manager import (
    ITelegramChat,
    ITelegramChatManager,
)
from core.tools import IDependencyInjector, IObserver
from core.tools.observer import IEvent
from telebot import types as tgt
from telegram import BotCommandEvent, tbot
from telegram.handlers.start import command_observable_component
from telegram.messages import txt

HOST = str(os.getenv("HOST"))


class StartController(IObserver):
    def __init__(self, engine_di_container: IDependencyInjector) -> None:
        super().__init__()

        telegram_chat_manager: t.Optional[
            ITelegramChatManager
        ] = engine_di_container.get_singleton(ITelegramChatManager)

        if telegram_chat_manager is None:
            raise ValueError("Can't get engine component for telegram chats")

        self.__telegram_chat_manager: ITelegramChatManager = telegram_chat_manager

        command_observable_component.add_observer(self)

    def __get_or_create_chat(self, chat_id: int) -> ITelegramChat:
        chat_instance: t.Optional[
            ITelegramChat
        ] = self.__telegram_chat_manager.get_chat(telegram_chat_id=chat_id)

        if chat_instance is not None:
            return chat_instance

        return self.__telegram_chat_manager.create_chat(chat_id)

    def notify(self, event: IEvent) -> None:
        if not isinstance(event, BotCommandEvent):
            return

        if event.command == "start":
            chat_instance: ITelegramChat = self.__get_or_create_chat(event.chat_id)

            tbot.send_message(
                event.chat_id, txt(chat_instance.language_code, "start_message")
            )
