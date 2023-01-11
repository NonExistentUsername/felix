import typing as t
from abc import ABC, abstractmethod

class IJsonable(ABC):
    @abstractmethod
    def to_json(self) -> t.Dict:
        pass

    @abstractmethod
    def from_json(self, json: t.Dict) -> None:
        pass