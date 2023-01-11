from abc import ABC, abstractmethod
from objects.engine import IEngineComponent
from objects.unique_object import ILinkedUniqueObject
from object_component import IObjectEngineComponent

class IPet(ILinkedUniqueObject):
    pass

class IPetEngineComponent(IObjectEngineComponent):
    pass