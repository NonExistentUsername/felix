import typing as t
from abc import abstractmethod

from objects.engine import IEngineComponent

class IDatabaseEngineComponent(IEngineComponent):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def save(self, data: t.Any) -> str:
        pass

    @abstractmethod
    def load(self, object_id: str) -> t.Any:
        pass


class IJsonDatabaseEngineComponent(IEngineComponent):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def save(self, data: t.Dict) -> str:
        pass

    @abstractmethod
    def load(self, object_id: str) -> t.Optional[t.Dict]:
        pass
