import logging
import os
import typing as t

from controller import IController
from core.tools import IDependencyInjector
from telebot import logger
from telebot import types as tgt

from .bot import tbot
from .controllers import (
    EconomyController,
    PetsController,
    SettingsController,
    StartController,
)
from .listeners import PetsListener

ENABLE_WEBHOOKS = os.getenv("ENABLE_WEBHOOKS") == "True"


class TelegramController(IController):
    def __init_controllers(self, engine_di_container: IDependencyInjector) -> None:
        self.__start_controller = StartController(engine_di_container)
        self.__settings_controller = SettingsController(engine_di_container)
        self.__pets_controller = PetsController(engine_di_container)
        self.__economy_controller = EconomyController(engine_di_container)

    def __init_listeners(self, engine_di_container: IDependencyInjector) -> None:
        self.__pets_listener = PetsListener(engine_di_container)

    def __init__(self, engine_di_container: IDependencyInjector) -> None:
        super().__init__()
        engine_di_container.register_singleton(logging.Logger, logger)

        self.__init_controllers(engine_di_container)
        self.__init_listeners(engine_di_container)

    def start(self) -> None:
        if ENABLE_WEBHOOKS:
            from webhooks import run_app

            run_app()
        else:
            tbot.infinity_polling()
