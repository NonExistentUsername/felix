import typing as t
from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal

from core.general.engine import IEngineComponent
from core.general.unique_object import ILinkedUniqueObject, IUniqueObject


class IPeriodicMoneyBonusInfo(ILinkedUniqueObject):
    @property
    @abstractmethod
    def last_collected_at(self) -> t.Optional[datetime]:
        pass

    @last_collected_at.setter
    @abstractmethod
    def last_collected_at(self, new_value: datetime) -> t.Optional[datetime]:
        pass


class ICollectionMethod(ABC):
    @abstractmethod
    def can_collect(self, last_collected_at: t.Optional[datetime]) -> bool:
        pass

    @abstractmethod
    def calc(self, last_collected_at: t.Optional[datetime]) -> Decimal:
        pass


class IPeriodicMoneyBonusInfoFactory(ABC):
    @abstractmethod
    def create(self, owner_id: int) -> IPeriodicMoneyBonusInfo:
        pass

    @abstractmethod
    def get(self, owner_id: int) -> t.Optional[IPeriodicMoneyBonusInfo]:
        pass

    @abstractmethod
    def delete(self, owner_id: int) -> IPeriodicMoneyBonusInfo:
        pass


class IPeriodicMoneyBonusEngineComponent(IEngineComponent):
    @abstractmethod
    def add_bonuses_for_object(self, owner_id: int) -> None:
        pass

    @abstractmethod
    def can_collect(self, owner_id: int) -> bool:
        pass

    @abstractmethod
    def collect(self, owner_id: int) -> Decimal:
        pass

    @abstractmethod
    def get_periodic_money_bonus_info(
        self, owner_id: int
    ) -> t.Optional[IPeriodicMoneyBonusInfo]:
        pass

    @abstractmethod
    def delete_periodic_money_bonus_info(
        self, owner_id: int
    ) -> IPeriodicMoneyBonusInfo:
        pass
