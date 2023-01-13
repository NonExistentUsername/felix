from controller.interfaces import IController
from core.engines import PetsEngine
from telegram.controller import TelegramController
import threading


class TelegramPetsMainController(IController):
    def __init__(self) -> None:
        super().__init__()

        self.__engine = PetsEngine()
        self.__engine_background_thread = threading.Thread(
            target=self.__engine.run, daemon=True
        )
        self.__telegram_controller = TelegramController(
            self.__engine.get_di_container()
        )

    def start(self) -> None:
        # start engine updating in background
        self.__engine_background_thread.start()

        self.__telegram_controller.start()
