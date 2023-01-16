import typing as t
import os
import logging
from telebot import types as tgt

from controller import IController
from core.tools import IDependencyInjector, IObserver, IEvent
from .handlers import command_observable_component
from .bot import tbot
from .events import BotCommandEvent
from .listeners import EngineUpdatesListener

from core.engine_components.pet_component import IPetEngineComponent
from core.engine_components.telegram_components.chat_manager import (
    ITelegramChatManager,
    ITelegramChat,
)
from .messages import txt


DEBUG = os.getenv("DEBUG") == "True"
logger = logging.Logger("*", logging.DEBUG)


class TelegramController(IController, IObserver):
    def __init__(self, engine_di_container: IDependencyInjector) -> None:
        super().__init__()

        telegram_chat_manager: t.Optional[
            ITelegramChatManager
        ] = engine_di_container.get_singleton(ITelegramChatManager)

        if telegram_chat_manager is None:
            raise ValueError("Can't get engine component for telegram chats")

        self.__telegram_chat_manager: ITelegramChatManager = telegram_chat_manager

        pet_engine_component: t.Optional[
            IPetEngineComponent
        ] = engine_di_container.get_singleton(IPetEngineComponent)

        if pet_engine_component is None:
            raise ValueError("Can't get engine component for pets")

        self.__pet_engine_component: IPetEngineComponent = pet_engine_component

        self.__pet_engine_component.add_observer(
            EngineUpdatesListener(engine_di_container)
        )

        command_observable_component.add_observer(self)

        self.__command_event_to_method = {
            "create_pet": self.__create_pet,
            "settings": self.__settings,
        }

    def __get_or_create_chat(self, chat_id: int) -> ITelegramChat:
        chat_instance: t.Optional[
            ITelegramChat
        ] = self.__telegram_chat_manager.get_chat(telegram_chat_id=chat_id)

        if chat_instance is not None:
            return chat_instance

        return self.__telegram_chat_manager.create_chat(chat_id)

    def __create_pet(self, command_event: BotCommandEvent) -> None:
        try:
            chat_id: int = int(command_event.kwargs["chat_id"])
        except Exception as e:
            logger.exception(e)
            return

        tg_chat: ITelegramChat = self.__get_or_create_chat(chat_id)

        if self.__pet_engine_component.get_pet(tg_chat.get_id()) is not None:
            tbot.send_message(
                chat_id, txt(tg_chat.language_code, "pet_already_created")
            )
            return

        self.__pet_engine_component.create_pet(tg_chat.get_id())

    def __settings_menu_markup(
        self, tg_chat: ITelegramChat
    ) -> tgt.InlineKeyboardMarkup:
        settings_menu = tgt.InlineKeyboardMarkup()
        settings_menu.add(
            tgt.InlineKeyboardButton(
                txt(tg_chat.language_code, "language_settings"),
                callback_data="open_language_settings",
            )
        )

        return settings_menu

    def __settings(self, command_event: BotCommandEvent) -> None:
        try:
            chat_id: int = int(command_event.kwargs["chat_id"])
        except Exception as e:
            logger.exception(e)
            return

        tg_chat: ITelegramChat = self.__get_or_create_chat(chat_id)

        tbot.send_message(
            chat_id,
            txt(tg_chat.language_code, "settings_menu"),
            reply_markup=self.__settings_menu_markup(tg_chat),
        )

    def notify(self, event: IEvent) -> None:
        if isinstance(event, BotCommandEvent):
            if event.command in self.__command_event_to_method:
                try:
                    self.__command_event_to_method[event.command](event)
                except Exception as e:
                    logger.exception(e)
            else:
                pass

    def start(self) -> None:
        tbot.infinity_polling()
