import typing as t
from abc import ABC, abstractmethod

from ...general.unique_object import ILinkedUniqueObject
from ...general.engine import IEngineComponent
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

class IHealthFactory(ABC):
    @abstractmethod
    def create_object(self, owner_object) -> IHealth:
        pass

class IHealthEngineComponent(IEngineComponent):
    @abstractmethod
    def register_object_component(self, object_engine_component: IObjectEngineComponent, health_factory: IHealthFactory) -> None:
        pass
    
    @abstractmethod
    def get_health(self, owner_id: int) -> t.Optional[IHealth]:
        pass