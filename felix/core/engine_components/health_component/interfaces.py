import typing as t
from abc import ABC, abstractmethod

from ...objects.unique_object import ILinkedUniqueObject
from ...objects.engine import IEngineComponent
from ..object_component import IObjectEngineComponent

class IHealth(ILinkedUniqueObject):
    @property
    @abstractmethod
    def health(self) -> int:
        pass

    @health.setter
    @abstractmethod
    def health(self, new_value: int) -> None:
        pass
    
    @property
    @abstractmethod
    def max_health(self) -> int:
        pass
    
    @max_health.setter
    @abstractmethod
    def max_health(self, new_value: int) -> None:
        pass

    @property
    @abstractmethod
    def min_health(self) -> int:
        pass
    
    @min_health.setter
    @abstractmethod
    def min_health(self, new_value: int) -> None:
        pass


class IHealthEngineComponent(IEngineComponent):
    @abstractmethod
    def register_object_component(self, object_engine_component: IObjectEngineComponent) -> None:
        pass
    
    @abstractmethod
    def get_health(self, owner_id: int) -> t.Optional[IHealth]:
        pass