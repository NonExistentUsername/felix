from abc import ABC, abstractmethod
import typing as t

from ..observer import Observable


class IEngineComponent(Observable):
    @abstractmethod
    def update_state(self, time_delta: float) -> None:
        pass

class IEngine(Observable):
    @abstractmethod
    def register_component(self, interface_type: type, object: IEngineComponent) -> None:
        pass

    @abstractmethod
    def get_component(self, interface_type: type) -> t.Optional['IEngineComponent']:
        pass

    @abstractmethod
    def update_state(self, time_delta: float) -> None:
        pass