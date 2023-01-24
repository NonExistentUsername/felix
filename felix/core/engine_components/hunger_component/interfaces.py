import typing as t
from abc import ABC, abstractmethod

from core.general.engine import IEngineComponent
from core.general.unique_object import ILinkedUniqueObject, IUniqueObject


class IHunger(ILinkedUniqueObject):
    @property
    @abstractmethod
    def value(self) -> float:
        pass

    @value.setter
    @abstractmethod
    def value(self, new_value: float) -> None:
        pass


class IHungerFactory(ABC):
    @abstractmethod
    def create(self, owner_id: int) -> IHunger:
        pass

    @abstractmethod
    def get(
        self,
        owner_id: t.Optional[int] = None,
        object_id: t.Optional[int] = None,
    ) -> t.Optional[IHunger]:
        pass

    @abstractmethod
    def delete(self, owner_id: int) -> IHunger:
        pass


class IHungerEngineComponent(IEngineComponent):
    @abstractmethod
    def create_hunger(self, owner_id: int) -> IHunger:
        pass

    @abstractmethod
    def create_or_get_hunger(self, owner_id: int) -> IHunger:
        pass

    @abstractmethod
    def get_hunger(
        self,
        owner_id: t.Optional[int] = None,
        object_id: t.Optional[int] = None,
    ) -> t.Optional[IHunger]:
        pass

    @abstractmethod
    def delete_hunger(self, owner_id: int) -> IHunger:
        pass
