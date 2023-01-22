import typing as t

from core.database import Base, database_session
from core.general.unique_object import IUniqueIDGenerator
from core.tools.dependency_injector import IDependencyInjector
from core.tools.observer import Observable
from sqlalchemy import DECIMAL, BigInteger, Column, Float, ForeignKey, Numeric, String

from .interfaces import IHunger, IHungerEngineComponent, IHungerFactory


class DBHungerModel(Base):
    __tablename__ = "hunger_param"

    id = Column(
        Numeric(40, 0),
        nullable=False,
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    owner_id = Column(Numeric(40, 0), nullable=False)
    value = Column(Float, nullable=False, server_default="0")


class DBHunger(IHunger):
    def __init__(self, db_instance: DBHungerModel) -> None:
        super().__init__()
        self.__db_instance = db_instance

    def get_id(self) -> int:
        return int(self.__db_instance.id)  # type: ignore

    def get_owner_id(self) -> int:
        return int(self.__db_instance.owner_id)  # type: ignore

    @property
    def value(self) -> float:
        return float(self.__db_instance.value)  # type: ignore

    @value.setter
    def value(self, new_value: float) -> None:
        if new_value < 0 or new_value > 100:
            raise ValueError("Value must be in range [0; 100]")

        with database_session() as db:
            db_instance: t.Optional[DBHungerModel] = db.query(DBHungerModel).filter(DBHungerModel.id == self.__db_instance.id).first()  # type: ignore

            if db_instance is None:
                return

            self.__db_instance = db_instance
            self.__db_instance.value = new_value
            db.commit()
            db.refresh(self.__db_instance)


class HungerFactory(IHungerFactory):
    def __init__(self, di_container: IDependencyInjector) -> None:
        super().__init__()
        id_generator: t.Optional[IUniqueIDGenerator] = di_container.get_singleton(
            IUniqueIDGenerator
        )
        if id_generator == None:
            raise ValueError("Can't get id generator from DI container")

        self.__id_generator: IUniqueIDGenerator = id_generator

    def create(self, owner_id: int) -> IHunger:
        with database_session() as db:
            hunger_instance: t.Optional[DBHungerModel] = (
                db.query(DBHungerModel)
                .filter(DBHungerModel.owner_id == owner_id)
                .first()
            )

            if hunger_instance is not None:
                raise ValueError("Chat already created")

            hunger_instance = DBHungerModel(
                id=self.__id_generator.create_id(),
                owner_id=owner_id,
            )
            db.add(hunger_instance)
            db.commit()
            db.refresh(hunger_instance)

            return DBHunger(hunger_instance)

    def get(
        self,
        owner_id: t.Optional[int] = None,
        object_id: t.Optional[int] = None,
    ) -> t.Optional[IHunger]:
        if owner_id is None and object_id is None:
            raise ValueError("Information not provided")

        with database_session() as db:
            db_query = db.query(DBHungerModel)

            if object_id:
                db_query = db_query.filter(DBHungerModel.id == object_id)

            if owner_id:
                db_query = db_query.filter(DBHungerModel.owner_id == owner_id)

            chat_instance: t.Optional[DBHungerModel] = db_query.first()

            if chat_instance is None:
                return None

            return DBHunger(chat_instance)


class HungerEngineComponent(IHungerEngineComponent, Observable):
    def __init__(self, hunger_factory: IHungerFactory) -> None:
        super().__init__()
        self.__hunger_factory = hunger_factory

    def create_hunger(self, owner_id: int) -> IHunger:
        return self.__hunger_factory.create(owner_id)

    def create_or_get_hunger(self, owner_id: int) -> IHunger:
        hunger_instance: t.Optional[IHunger] = self.get_hunger(owner_id=owner_id)

        if hunger_instance is not None:
            return hunger_instance

        hunger_instance = self.create_hunger(owner_id)

        return hunger_instance

    def get_hunger(
        self,
        owner_id: t.Optional[int] = None,
        object_id: t.Optional[int] = None,
    ) -> t.Optional[IHunger]:
        return self.__hunger_factory.get(owner_id, object_id)

    def update_state(self, time_delta: float) -> None:
        pass
