import typing as t
from abc import ABC, abstractmethod

from core.general.engine import IEngineComponent
from core.general.unique_object import ILinkedUniqueObject, IUniqueObject


class IVivacity(ILinkedUniqueObject):
    @property
    @abstractmethod
    def value(self) -> float:
        pass

    @value.setter
    @abstractmethod
    def value(self, new_value: float) -> None:
        pass


class IVivacityFactory(ABC):
    @abstractmethod
    def create(self, owner_id: int) -> IVivacity:
        pass

    @abstractmethod
    def get(
        self,
        owner_id: t.Optional[int] = None,
        object_id: t.Optional[int] = None,
    ) -> t.Optional[IVivacity]:
        pass


class IVivacityEngineComponent(IEngineComponent):
    @abstractmethod
    def create_vivacity(self, owner_id: int) -> IVivacity:
        pass

    @abstractmethod
    def create_or_get_vivacity(self, owner_id: int) -> IVivacity:
        pass

    @abstractmethod
    def get_vivacity(
        self,
        owner_id: t.Optional[int] = None,
        object_id: t.Optional[int] = None,
    ) -> t.Optional[IVivacity]:
        pass
