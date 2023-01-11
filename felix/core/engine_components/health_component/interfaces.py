from abc import ABC, abstractmethod

from objects.unique_object import ILinkedUniqueObject
from objects.engine import IEngineComponent
from object_component import IObjectEngineComponent

class IHealthEngineComponent(IEngineComponent):
    @abstractmethod
    def register_object_component(self, object_engine_component: IObjectEngineComponent) -> None:
        pass