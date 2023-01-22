from general.engine import IEngine, IEngineFactory

from .engines import PetsEngine


class PetsEngineFactory(IEngineFactory):
    def __init__(self) -> None:
        super().__init__()

    def create(self) -> IEngine:
        return PetsEngine()
