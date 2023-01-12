from abc import ABC, abstractmethod

from ...general.engine import IEngineComponent

class IPlayer(ABC):
    @property
    @abstractmethod
    def get_id(self) -> str:
        pass

class IPlayersComponent(IEngineComponent):
    pass