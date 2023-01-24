import typing as t
from abc import ABC, abstractmethod
from decimal import Decimal

from core.general.engine import IEngineComponent
from core.general.unique_object import ILinkedUniqueObject, IUniqueObject


class IBalance(ILinkedUniqueObject):
    @property
    @abstractmethod
    def value(self) -> Decimal:
        pass

    @value.setter
    @abstractmethod
    def value(self, new_value: Decimal) -> None:
        pass


class IBalanceFactory(ABC):
    @abstractmethod
    def create(self, owner_id: int) -> IBalance:
        pass

    @abstractmethod
    def get(
        self,
        owner_id: t.Optional[int] = None,
        object_id: t.Optional[int] = None,
    ) -> t.Optional[IBalance]:
        pass

    @abstractmethod
    def delete(self, owner_id: int) -> IBalance:
        pass


class IEconomyEngineComponent(IEngineComponent):
    @abstractmethod
    def create_balance(self, owner_id: int) -> IBalance:
        pass

    @abstractmethod
    def create_or_get_balance(self, owner_id: int) -> IBalance:
        pass

    @abstractmethod
    def get_balance(
        self,
        owner_id: t.Optional[int] = None,
        object_id: t.Optional[int] = None,
    ) -> t.Optional[IBalance]:
        pass

    @abstractmethod
    def delete_balance(self, owner_id: int) -> IBalance:
        pass
