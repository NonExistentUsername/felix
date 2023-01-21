import typing as t
import os
import logging
from telebot import types as tgt

from controller import IController
from core.tools import IDependencyInjector, IObserver, IEvent
from telegram.handlers.pets import command_observable_component
from telegram import tbot, BotCommandEvent, BotCallbackEvent

from core.engine_components.pet_component import IPetEngineComponent
from core.engine_components.telegram_components.chat_manager import (
    ITelegramChatManager,
    ITelegramChat,
)
from core.engine_components.pet_customization_component import (
    IPetCustomizationEngineComponent,
)
from telegram.messages import txt


class PetsController(IObserver):
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

        command_observable_component.add_observer(self)

    def __get_or_create_chat(self, chat_id: int) -> ITelegramChat:
        chat_instance: t.Optional[
            ITelegramChat
        ] = self.__telegram_chat_manager.get_chat(telegram_chat_id=chat_id)

        if chat_instance is not None:
            return chat_instance

        return self.__telegram_chat_manager.create_chat(chat_id)

    def __create_pet_command(self, event: BotCommandEvent) -> None:
        chat_instance: ITelegramChat = self.__get_or_create_chat(event.chat_id)

        if self.__pet_engine_component.get_pet(chat_instance.get_id()) is not None:
            tbot.send_message(
                event.chat_id,
                txt(chat_instance.language_code, "pet_already_created"),
            )
            return

        self.__pet_engine_component.create_pet(chat_instance.get_id())

    def notify(self, event: IEvent) -> None:
        if not isinstance(event, BotCommandEvent):
            return

        if event.command == "create_pet":
            self.__create_pet_command(event)
