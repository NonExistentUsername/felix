import typing as t
from abc import ABC, abstractmethod


class IDependencyInjector(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def register_singleton(self, interface_type: type, object) -> None:
        pass

    @abstractmethod
    def get_singleton(self, interface_type: type):
        pass
