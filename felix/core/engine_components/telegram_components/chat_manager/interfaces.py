import typing as t

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
    def create_chat(self, chat_id: int) -> ITelegramChat:
        pass

    @abstractmethod
    def get_chat(
        self,
        object_id: t.Optional[int] = None,
        telegram_chat_id: t.Optional[int] = None,
    ) -> t.Optional[ITelegramChat]:
        pass
