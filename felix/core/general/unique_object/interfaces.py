from abc import ABC, abstractmethod

class IUniqueIDGenerator(ABC):
    @abstractmethod
    def create_id(self) -> int:
        pass

class IUniqueObject(ABC):
    @abstractmethod
    def get_id(self) -> int:
        pass

class ILinkedUniqueObject(IUniqueObject):
    @abstractmethod
    def get_owner_id(self) -> int:
        pass