from abc import ABC, abstractmethod

class IUniqueIDGenerator(ABC):
    @abstractmethod
    def create_id(self) -> int:
        pass

class UniqueObject(ABC):
    @abstractmethod
    def get_id(self) -> int:
        pass

class LinkedUniqueObject(UniqueObject):
    @abstractmethod
    def get_owner_id(self) -> int:
        pass