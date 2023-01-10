import typing as t
from abc import abstractmethod

from objects.engine import IEngineComponent

class IDatabaseEngineComponent(IEngineComponent):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def save(self, table_name: str, data: t.Any) -> int:
        pass

    @abstractmethod
    def load(self, table_name: str, object_id: int) -> t.Any:
        pass


class IJsonDatabaseEngineComponent(IEngineComponent):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def save(self, table_name: str, data: t.Dict) -> int:
        pass

    @abstractmethod
    def load(self, table_name: str, object_id: int) -> t.Optional[t.Dict]:
        pass
