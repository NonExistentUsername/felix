from general.engine import IEngineFactory, IEngine
from .engines import PetsEngine


class PetsEngineFactory(IEngineFactory):
    def __init__(self) -> None:
        super().__init__()

    def create(self) -> IEngine:
        return PetsEngine()
