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
    def create(self, type: str) -> IPet:
        pass

class IPetEngineComponent(IObjectEngineComponent):
    pass