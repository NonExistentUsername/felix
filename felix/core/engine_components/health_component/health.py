from .interfaces import IHealth
from core.general.unique_object.mixins import LinkedUniqueObjectMixin


class Health(IHealth, LinkedUniqueObjectMixin):
    def __init__(
        self,
        id: int,
        owner_id: int,
        health: int,
        min_health: int = 0,
        max_health: int = 100,
    ) -> None:
        super().__init__(id=id, owner_id=owner_id)
        self.__health = health
        self.__min_health = min_health
        self.__max_health = max_health

    @property
    def health(self) -> int:
        return self.__health

    @health.setter
    def health(self, new_value: int) -> None:
        if new_value < self.__min_health:
            raise ValueError(f"Min health value: {self.__min_health}")
        if new_value > self.__max_health:
            raise ValueError(f"Max health value: {self.__max_health}")
        self.__health = new_value

    @property
    def max_health(self) -> int:
        return self.__max_health

    @max_health.setter
    def max_health(self, new_value: int) -> None:
        if new_value < self.__min_health:
            raise ValueError(f"Min max_health value: {self.__max_health}")
        self.__max_health = new_value

    @property
    def min_health(self) -> int:
        return self.__min_health

    @min_health.setter
    def min_health(self, new_value: int) -> None:
        if new_value > self.__max_health:
            raise ValueError(f"Max min_health value: {self.__max_health}")
        self.__min_health = new_value
