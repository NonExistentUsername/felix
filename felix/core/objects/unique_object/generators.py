from uuid import uuid1

from .interfaces import IUniqueIDGenerator

class UUID1(IUniqueIDGenerator):
    def create_id(self) -> int:
        return uuid1().int