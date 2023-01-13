import typing as t
from abc import ABC, abstractmethod


class IController(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def start(self) -> None:
        pass
