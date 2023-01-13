import typing as t
from sqlalchemy import Column, String, Integer, ForeignKey

from ....general.unique_object import UniqueObjectMixin, IUniqueIDGenerator
from ....tools.dependency_injector import IDependencyInjector
from ....database import Base, database_session

from .interfaces import ITelegramChat, ITelegramChatManager


class DBTelegramChatModel(Base):
    __tablename__ = "talagram_chat"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, index=True)


class DBTelegramChat(ITelegramChat, UniqueObjectMixin):
    def __init__(self, instance: DBTelegramChatModel) -> None:
        super().__init__(id=int(instance.id))  # type: ignore
        self.__db_instance = instance

    @property
    def chat_id(self) -> int:
        return int(self.__db_instance.chat_id)  # type: ignore


class TelegramChatManager(ITelegramChatManager):
    def __init__(self, di_container: IDependencyInjector) -> None:
        super().__init__()
        id_generator: t.Optional[IUniqueIDGenerator] = di_container.get_singleton(
            IUniqueIDGenerator
        )
        if id_generator == None:
            raise ValueError("Can't get id generator from DI container")

        self.__id_generator: IUniqueIDGenerator = id_generator

    def get_chat(self, chat_id: int) -> ITelegramChat:
        with database_session() as db:
            chat_instance: t.Optional[DBTelegramChatModel] = (
                db.query(DBTelegramChatModel)
                .filter(DBTelegramChatModel.chat_id == chat_id)
                .first()
            )

            if chat_instance is None:
                chat_instance = DBTelegramChatModel(
                    id=self.__id_generator.create_id(), chat_id=chat_id
                )
                db.add(chat_instance)
                db.commit()
                db.refresh(chat_instance)

            return DBTelegramChat(chat_instance)
