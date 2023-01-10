from abc import ABC, abstractmethod

class IUniqueIDGenerator(ABC):
    @abstractmethod
    def get_id(self) -> str:
        pass