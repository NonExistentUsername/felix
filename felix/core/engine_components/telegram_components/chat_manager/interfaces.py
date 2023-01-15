import typing as t

from abc import ABC, abstractmethod
from core.general.engine import IEngineComponent
from core.general.unique_object import IUniqueObject


class ITelegramChat(IUniqueObject):
    @property
    @abstractmethod
    def chat_id(self) -> int:
        pass

    @property
    @abstractmethod
    def language_code(self) -> str:
        pass

    @language_code.setter
    @abstractmethod
    def language_code(self, new_language_code: str) -> None:
        pass


class ITelegramChatManager(IEngineComponent):
    @abstractmethod
    def create_chat(self, telegram_chat_id: int) -> ITelegramChat:
        pass

    @abstractmethod
    def get_chat(
        self,
        object_id: t.Optional[int] = None,
        telegram_chat_id: t.Optional[int] = None,
    ) -> t.Optional[ITelegramChat]:
        pass
