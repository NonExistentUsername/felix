from abc import ABC, abstractmethod
from objects.engine import IEngineComponent
from objects.unique_object import ILinkedUniqueObject
from object_component import IObjectEngineComponent

class IPet(ILinkedUniqueObject):
    pass

class IPetEngineComponent(IObjectEngineComponent):
    @abstractmethod
    def create_object(self, owner_id: int) -> IPet:
        pass