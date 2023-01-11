from .interfaces import ILinkedUniqueObject, IUniqueObject

class UniqueObjectMixin(IUniqueObject):
    def __init__(self, id: int) -> None:
        super().__init__()
        self.__id = id

    def get_id(self) -> int:
        return self.__id

class LinkedUniqueObjectMixin(ILinkedUniqueObject, UniqueObjectMixin):
    def __init__(self, id: int, owner_id: int) -> None:
        super().__init__(id)
        self.__owner_id = owner_id
    
    def get_owner_id(self) -> int:
        return self.__owner_id