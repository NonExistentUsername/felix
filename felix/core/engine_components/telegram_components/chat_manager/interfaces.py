from abc import ABC, abstractmethod
from ....general.engine import IEngineComponent
from ....general.unique_object import IUniqueObject

class ITelegramChat(IUniqueObject):
    @property
    @abstractmethod
    def chat_id(self) -> int:
        pass

class ITelegramChatManager(IEngineComponent):
    @abstractmethod
    def get_chat(self, chat_id: int) -> ITelegramChat:
        pass