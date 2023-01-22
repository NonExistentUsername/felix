import logging
import os
import typing as t

from controller import IController
from core.engine_components.pet_component import IPet, IPetEngineComponent
from core.engine_components.pet_customization_component import (
    IPetCustomization,
    IPetCustomizationEngineComponent,
)
from core.engine_components.telegram_components.chat_manager import (
    ITelegramChat,
    ITelegramChatManager,
)
from core.tools import IDependencyInjector, IEvent, IObserver
from telebot import types as tgt
from telegram import BotCallbackEvent, BotCommandEvent, tbot
from telegram.handlers.pets import command_observable_component
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

        cutomization_engine_component: t.Optional[
            IPetCustomizationEngineComponent
        ] = engine_di_container.get_singleton(IPetCustomizationEngineComponent)

        if cutomization_engine_component is None:
            raise ValueError("Can't get customization engine component for pets")

        self.__cutomization_engine_component: IPetCustomizationEngineComponent = (
            cutomization_engine_component
        )

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

    def __pet_set_name_command(self, event: BotCommandEvent) -> None:
        try:
            new_name: str = event.kwargs["new_name"]
        except Exception as e:
            return

        chat_instance: ITelegramChat = self.__get_or_create_chat(event.chat_id)

        if len(new_name) == 0 or len(new_name) > 63:
            tbot.send_message(
                event.chat_id, txt(chat_instance.language_code, "pet_set_name_tutorial")
            )
            return

        pet: t.Optional[IPet] = self.__pet_engine_component.get_pet(
            chat_instance.get_id()
        )

        if pet is None:
            tbot.send_message(
                event.chat_id, txt(chat_instance.language_code, "create_pet_first")
            )
            return

        pets_customization: IPetCustomization = (
            self.__cutomization_engine_component.get_pet_customization(pet.get_id())
        )

        pets_customization.name = new_name

    def notify(self, event: IEvent) -> None:
        if not isinstance(event, BotCommandEvent):
            return

        if event.command == "create_pet":
            self.__create_pet_command(event)
        elif event.command == "set_pet_name":
            self.__pet_set_name_command(event)
