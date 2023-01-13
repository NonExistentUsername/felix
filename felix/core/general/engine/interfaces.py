from abc import ABC, abstractmethod
import typing as t

from core.tools.observer import IObservable
from core.tools.dependency_injector import IDependencyInjector


class IEngineComponent(IObservable):
    @abstractmethod
    def update_state(self, time_delta: float) -> None:
        pass


class IEngine(ABC):
    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def get_di_container(self) -> IDependencyInjector:
        pass


class IEngineFactory(ABC):
    @abstractmethod
    def create(self) -> IEngine:
        pass
