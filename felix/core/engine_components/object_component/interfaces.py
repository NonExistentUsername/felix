import typing as t
from abc import abstractmethod

from ...general.engine import IEngineComponent

class IObjectEngineComponent(IEngineComponent):
    @abstractmethod
    def create_object(self, *args, **kwargs) -> t.Any:
        pass