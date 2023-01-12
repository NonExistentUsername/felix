import typing as t
from abc import ABC, abstractmethod
from general.engine import IEngineComponent
from general.unique_object import ILinkedUniqueObject
from object_component import IObjectEngineComponent

class IPet(ILinkedUniqueObject):
    @property
    @abstractmethod
    def type(self) -> str:
        pass

class IPetFactory(ABC):
    @abstractmethod
    def create(self, owner_id: int) -> IPet:
        pass

class IPetEngineComponent(IObjectEngineComponent):
    @abstractmethod
    def get_pet(self, owner_id: int) -> t.Optional[IPet]:
        pass