import typing as t

from ..controller import IController
from ..core.tools import IDependencyInjector, IObserver, IEvent
from .handlers import command_observable_component
from .bot import tbot
from .events import BotCommandEvent

from ..core.engine_components.pet_component import IPetEngineComponent
from ..core.engine_components.telegram_components.chat_manager import (
    ITelegramChatManager,
)


class TelegramController(IController, IObserver):
    def __init__(self, engine_di_controller: IDependencyInjector) -> None:
        super().__init__()
        pet_engine_component: t.Optional[
            IPetEngineComponent
        ] = engine_di_controller.get_singleton(IPetEngineComponent)

        if pet_engine_component is None:
            raise ValueError("Can't get engine component for pets")

        self.__pet_engine_component: IPetEngineComponent = pet_engine_component

        telegram_chat_manager: t.Optional[
            ITelegramChatManager
        ] = engine_di_controller.get_singleton(ITelegramChatManager)

        if telegram_chat_manager is None:
            raise ValueError("Can't get engine component for telegram chats")

        self.__telegram_chat_manager: ITelegramChatManager = telegram_chat_manager

    def notify(self, event: IEvent) -> None:
        if not isinstance(event, BotCommandEvent):
            return

        if event.command == "create_pet":
            self.__pet_engine_component.create_pet(
                self.__telegram_chat_manager.get_chat(event.kwargs["chat_id"]).get_id()
            )

    def start(self) -> None:
        tbot.infinity_polling()
