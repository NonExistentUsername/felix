import typing as t
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


class IPetCustomizationFactory(ABC):
    @abstractmethod
    def get(self, pet_id: int) -> t.Optional[IPetCustomization]:
        pass

    @abstractmethod
    def create(self, pet_id: int) -> IPetCustomization:
        pass


class IPetCustomizationEngineComponent(IEngineComponent):
    @abstractmethod
    def get_pet_customization(self, pet_id: int) -> IPetCustomization:
        pass
