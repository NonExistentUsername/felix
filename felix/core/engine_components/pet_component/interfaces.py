import typing as t
from abc import ABC, abstractmethod

from core.general.engine import IEngineComponent
from core.general.unique_object import ILinkedUniqueObject


class IPet(ILinkedUniqueObject):
    @property
    @abstractmethod
    def type(self) -> str:
        pass


class IPetFactory(ABC):
    @abstractmethod
    def create(self, owner_id: int) -> IPet:
        pass

    @abstractmethod
    def get(
        self,
        owner_id: t.Optional[int] = None,
        pet_id: t.Optional[int] = None,
    ) -> t.Optional[IPet]:
        pass


class IPetEngineComponent(IEngineComponent):
    @abstractmethod
    def create_pet(self, owner_id: int) -> IPet:
        pass

    @abstractmethod
    def get_pet(
        self,
        owner_id: t.Optional[int] = None,
        pet_id: t.Optional[int] = None,
    ) -> t.Optional[IPet]:
        pass
