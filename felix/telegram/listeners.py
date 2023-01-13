import typing as t
from abc import ABC, abstractmethod

from .bot import tbot

from core.tools.observer import IObserver, IEvent
from core.tools.dependency_injector import IDependencyInjector
from core.engine_components.pet_component import PetCreated
from core.engine_components.telegram_components.chat_manager import (
    ITelegramChatManager,
    ITelegramChat,
)


class EngineUpdatesListener(IObserver):
    def __init__(self, engine_di_container: IDependencyInjector) -> None:
        super().__init__()

        telegram_chat_manager: t.Optional[
            ITelegramChatManager
        ] = engine_di_container.get_singleton(ITelegramChatManager)

        if telegram_chat_manager is None:
            raise ValueError("Can't get engine component for telegram chats")

        self.__telegram_chat_manager: ITelegramChatManager = telegram_chat_manager

    def notify(self, event: IEvent) -> None:
        if isinstance(event, PetCreated):
            chat_instance: t.Optional[
                ITelegramChat
            ] = self.__telegram_chat_manager.get_chat(
                object_id=event.get_instance().get_owner_id()
            )

            if chat_instance is None:
                return

            tbot.send_message(chat_instance.chat_id, "Pet created.")
