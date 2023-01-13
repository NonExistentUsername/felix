import typing as t

from ..controller import IController
from ..core.tools import IDependencyInjector, IObserver, IEvent
from .handlers import command_observable_component
from .bot import tbot
from .events import BotCommandEvent
from .listeners import EngineUpdatesListener

from ..core.engine_components.pet_component import IPetEngineComponent
from ..core.engine_components.telegram_components.chat_manager import (
    ITelegramChatManager,
    ITelegramChat,
)


class TelegramController(IController, IObserver):
    def __init__(self, engine_di_container: IDependencyInjector) -> None:
        super().__init__()
        pet_engine_component: t.Optional[
            IPetEngineComponent
        ] = engine_di_container.get_singleton(IPetEngineComponent)

        if pet_engine_component is None:
            raise ValueError("Can't get engine component for pets")

        self.__pet_engine_component: IPetEngineComponent = pet_engine_component

        self.__pet_engine_component.add_observer(
            EngineUpdatesListener(engine_di_container)
        )

        telegram_chat_manager: t.Optional[
            ITelegramChatManager
        ] = engine_di_container.get_singleton(ITelegramChatManager)

        if telegram_chat_manager is None:
            raise ValueError("Can't get engine component for telegram chats")

        self.__telegram_chat_manager: ITelegramChatManager = telegram_chat_manager

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

        if event.command == "create_pet":
            self.__pet_engine_component.create_pet(
                self.__get_or_create_chat(event.kwargs["chat_id"]).get_id()
            )

    def start(self) -> None:
        tbot.infinity_polling()
