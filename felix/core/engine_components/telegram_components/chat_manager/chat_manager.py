import typing as t

from core.database import Base, database_session
from core.general.unique_object import IUniqueIDGenerator, UniqueObjectMixin
from core.tools.dependency_injector import IDependencyInjector
from core.tools.observer import Observable
from sqlalchemy import BigInteger, Column, ForeignKey, Numeric, String

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
    language_code = Column(String(3), server_default="en")


class DBTelegramChat(ITelegramChat, UniqueObjectMixin):
    def __init__(self, instance: DBTelegramChatModel) -> None:
        super().__init__(id=int(instance.id))  # type: ignore
        self.__db_instance: DBTelegramChatModel = instance

    @property
    def chat_id(self) -> int:
        return int(self.__db_instance.chat_id)  # type: ignore

    @property
    def language_code(self) -> str:
        return str(self.__db_instance.language_code)

    @language_code.setter
    def language_code(self, new_language_code: str) -> None:
        if len(new_language_code) == "":
            raise ValueError("Can't set empty language code")

        if len(new_language_code) > 3:
            raise ValueError("Can't set language code longer than 3 characters")

        with database_session() as db:
            db_instance: t.Optional[DBTelegramChatModel] = db.query(DBTelegramChatModel).filter(DBTelegramChatModel.id == self.__db_instance.id).first()  # type: ignore
            if db_instance is None:
                return

            self.__db_instance = db_instance
            self.__db_instance.language_code = new_language_code
            db.commit()
            db.refresh(self.__db_instance)


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
                id=self.__id_generator.create_id(),
                chat_id=telegram_chat_id,
                language_code="en",
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
                db_query = db_query.filter(DBTelegramChatModel.id == object_id)

            if telegram_chat_id:
                db_query = db_query.filter(
                    DBTelegramChatModel.chat_id == telegram_chat_id
                )

            chat_instance: t.Optional[DBTelegramChatModel] = db_query.first()

            if chat_instance is None:
                return None

            return DBTelegramChat(chat_instance)

    def update_state(self, time_delta: float) -> None:
        pass
