from abc import ABC, abstractmethod

from core.general.engine import IEngineComponent
from core.general.unique_object import IUniqueObject


class IPetCustomization(IUniqueObject):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, new_name: str) -> None:
        pass


class IPetCustomizationComponent(IEngineComponent):
    @abstractmethod
    def get_pet_customization(self, pet_id: int) -> IPetCustomization:
        pass
