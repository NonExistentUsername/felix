import typing as t
import os
import logging
from telebot import types as tgt

from controller import IController
from core.tools import IDependencyInjector
from .bot import tbot
from .controllers import PetsController, StartController, SettingsController


class TelegramController(IController):
    def __init__(self, engine_di_container: IDependencyInjector) -> None:
        super().__init__()

        self.__start_controller = StartController(engine_di_container)
        self.__settings_controller = SettingsController(engine_di_container)
        self.__pets_controller = PetsController(engine_di_container)

    def start(self) -> None:
        tbot.infinity_polling()
