from abc import ABC, abstractmethod

from ...tools.observer import IEvent


class ObjectCreated(IEvent):
    def __init__(self, instance) -> None:
        super().__init__()
        self.__instance = instance

    def get_instance(self):
        return self.__instance
