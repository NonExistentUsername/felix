import typing as t
import os
import logging

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

from core.tools.dependency_injector import IDependencyInjector
from .events import BotCommandEvent
from .messages import txt

DEBUG = os.getenv("DEBUG") == "True"
logger = logging.Logger("*", logging.DEBUG)


class BotCommandsController:
    def __init__(self, engine_di_container: IDependencyInjector) -> None:
        pet_engine_component: t.Optional[
            IPetEngineComponent
        ] = engine_di_container.get_singleton(IPetEngineComponent)

        if pet_engine_component is None:
            raise ValueError("Can't get engine component for pets")

        self.__pet_engine_component: IPetEngineComponent = pet_engine_component

        telegram_chat_manager: t.Optional[
            ITelegramChatManager
        ] = engine_di_container.get_singleton(ITelegramChatManager)

        if telegram_chat_manager is None:
            raise ValueError("Can't get engine component for telegram chats")

        self.__telegram_chat_manager: ITelegramChatManager = telegram_chat_manager

        self.__command_event_to_method = {"create_pet": self.__create_pet}

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
            tbot.send_message(chat_id, txt("ua", "pet_already_created"))
            return

        self.__pet_engine_component.create_pet(tg_chat.get_id())

    def process_command(self, command_event: BotCommandEvent) -> None:
        if command_event.command in self.__command_event_to_method:
            try:
                self.__command_event_to_method[command_event.command](command_event)
            except Exception as e:
                logger.exception(e)
        else:
            logging.exception(ValueError("ignored"))
