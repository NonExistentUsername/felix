from abc import ABC, abstractmethod
import typing as t

from ..observer import Observable


class IEngineComponent(Observable):
    @abstractmethod
    def update_state(self, time_delta: float) -> None:
        pass

class IEngine(ABC):
    @abstractmethod
    def run(self) -> None:
        pass

class IEngineFactory(ABC):
    @abstractmethod
    def create(self) -> IEngine:
        pass