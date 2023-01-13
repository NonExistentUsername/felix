import typing as t
from sqlalchemy import Column, String, BigInteger, ForeignKey, Numeric

from core.general.unique_object import UniqueObjectMixin, IUniqueIDGenerator
from core.tools.dependency_injector import IDependencyInjector
from core.tools.observer import Observable
from core.database import Base, database_session

from .interfaces import ITelegramChat, ITelegramChatManager


class DBTelegramChatModel(Base):
    __tablename__ = "talagram_chat"

    id = Column(
        Numeric(40, 0),
        nullable=False,
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    chat_id = Column(Numeric(40, 0), nullable=False)


class DBTelegramChat(ITelegramChat, UniqueObjectMixin):
    def __init__(self, instance: DBTelegramChatModel) -> None:
        super().__init__(id=int(instance.id))  # type: ignore
        self.__db_instance = instance

    @property
    def chat_id(self) -> int:
        return int(self.__db_instance.chat_id)  # type: ignore


class TelegramChatManager(ITelegramChatManager, Observable):
    def __init__(self, di_container: IDependencyInjector) -> None:
        super().__init__()
        id_generator: t.Optional[IUniqueIDGenerator] = di_container.get_singleton(
            IUniqueIDGenerator
        )
        if id_generator == None:
            raise ValueError("Can't get id generator from DI container")

        self.__id_generator: IUniqueIDGenerator = id_generator

    def create_chat(self, telegram_chat_id: int) -> ITelegramChat:
        with database_session() as db:
            chat_instance: t.Optional[DBTelegramChatModel] = (
                db.query(DBTelegramChatModel)
                .filter(DBTelegramChatModel.chat_id == telegram_chat_id)
                .first()
            )

            if chat_instance is not None:
                raise ValueError("Chat already created")

            chat_instance = DBTelegramChatModel(
                id=self.__id_generator.create_id(), chat_id=telegram_chat_id
            )
            db.add(chat_instance)
            db.commit()
            db.refresh(chat_instance)

            return DBTelegramChat(chat_instance)

    def get_chat(
        self,
        object_id: t.Optional[int] = None,
        telegram_chat_id: t.Optional[int] = None,
    ) -> t.Optional[ITelegramChat]:
        if object_id is None and telegram_chat_id is None:
            raise ValueError("Information not provided")

        with database_session() as db:
            db_query = db.query(DBTelegramChatModel)

            if object_id:
                db_query.filter(DBTelegramChatModel.id == object_id)

            if telegram_chat_id:
                db_query.filter(DBTelegramChatModel.chat_id == telegram_chat_id)

            chat_instance: t.Optional[DBTelegramChatModel] = db_query.first()

            if chat_instance is None:
                return None

            return DBTelegramChat(chat_instance)

    def update_state(self, time_delta: float) -> None:
        pass
