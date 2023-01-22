import logging
import typing as t
from abc import ABC, abstractmethod

from core.engine_components.pet_component import IPet, IPetEngineComponent, PetCreated
from core.engine_components.pet_customization_component import (
    IPetCustomizationEngineComponent,
)
from core.engine_components.pet_customization_component import (
    NameChanged as PetsNameChanged,
)
from core.engine_components.telegram_components.chat_manager import (
    ITelegramChat,
    ITelegramChatManager,
)
from core.tools.dependency_injector import IDependencyInjector
from core.tools.observer import IEvent, IObserver

from ..bot import tbot
from ..messages import txt


class PetsListener(IObserver):
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
        self.__pet_engine_component.add_observer(self)

        pet_customization_engine_component: t.Optional[
            IPetCustomizationEngineComponent
        ] = engine_di_container.get_singleton(IPetCustomizationEngineComponent)

        if pet_customization_engine_component is None:
            raise ValueError("Can't get customization engine component for pets")

        self.__pet_customization_engine_component: IPetCustomizationEngineComponent = (
            pet_customization_engine_component
        )
        self.__pet_customization_engine_component.add_observer(self)

        self.__logger: t.Optional[logging.Logger] = engine_di_container.get_singleton(
            logging.Logger
        )

    def notify(self, event: IEvent) -> None:
        if isinstance(event, PetCreated):
            chat_instance: t.Optional[
                ITelegramChat
            ] = self.__telegram_chat_manager.get_chat(
                object_id=event.get_instance().get_owner_id()
            )

            if chat_instance is None:
                return

            tbot.send_message(
                chat_instance.chat_id, txt(chat_instance.language_code, "pet_created")
            )
        elif isinstance(event, PetsNameChanged):
            pet: t.Optional[IPet] = self.__pet_engine_component.get_pet(
                event.pet_customization_instance.get_owner_id()
            )

            if not pet:
                return

            chat_instance: t.Optional[
                ITelegramChat
            ] = self.__telegram_chat_manager.get_chat(object_id=pet.get_owner_id())

            if chat_instance is None:
                return

            tbot.send_message(
                chat_instance.chat_id,
                txt(chat_instance.language_code, "pets_name_changed").format(
                    new_name=event.new_name
                ),
            )
