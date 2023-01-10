from abc import ABC, abstractmethod
import typing as t

from ..observer import Observable
from ..engine import IEngine

class IEngine(Observable):
    @abstractmethod
    def update(self, time_delta: float) -> None:
        pass

class IEngineComponent(IEngine):
    @abstractmethod
    def add_component(self, component: 'IEngineComponent') -> None:
        pass

    @abstractmethod
    def get_component(self, component_interface_type: type) -> t.Optional['IEngineComponent']:
        pass
