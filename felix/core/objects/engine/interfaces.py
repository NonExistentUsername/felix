from abc import ABC, abstractmethod
import typing as t

from ..observer import Observable


class IEngineComponent(Observable):
    @abstractmethod
    def update_state(self, time_delta: float) -> None:
        pass
