from abc import ABC, abstractmethod

from objects.engine import IEngineComponent

class IPlayer(ABC):
    @property
    @abstractmethod
    def get_id(self) -> str:
        pass

class IPlayersComponent(IEngineComponent):
    pass