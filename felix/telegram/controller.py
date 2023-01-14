import typing as t

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
from .commands_controller import BotCommandsController


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

        command_observable_component.add_observer(self)

        self.__bot_commands_controller = BotCommandsController(engine_di_container)

    def notify(self, event: IEvent) -> None:
        if isinstance(event, BotCommandEvent):
            self.__bot_commands_controller.process_command(event)

    def start(self) -> None:
        tbot.infinity_polling()
