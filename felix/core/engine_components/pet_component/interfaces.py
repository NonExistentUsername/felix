from abc import ABC, abstractmethod
from objects.engine import IEngineComponent
from objects.unique_object import ILinkedUniqueObject

class IPet(ILinkedUniqueObject):
    pass

class IPetEngineComponent(IEngineComponent):
    @abstractmethod
    def create_pet(self) -> IPet:
        pass