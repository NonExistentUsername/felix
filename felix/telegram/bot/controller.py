from ...controller import IController
from ...core.tools import IDependencyInjector

class TelegramController(IController):
    def __init__(self, engine_di_controller: IDependencyInjector) -> None:
        super().__init__()
        

    def start(self) -> None:
        pass