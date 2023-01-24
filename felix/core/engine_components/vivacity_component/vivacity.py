import typing as t

from core.database import Base, database_session
from core.general.unique_object import IUniqueIDGenerator, LinkedUniqueObjectMixin
from core.tools.dependency_injector import IDependencyInjector
from core.tools.observer import Observable
from sqlalchemy import DECIMAL, BigInteger, Column, Float, ForeignKey, Numeric, String

from .interfaces import IVivacity, IVivacityEngineComponent, IVivacityFactory


class DBVivacityModel(Base):
    __tablename__ = "vivacity_param"

    id = Column(
        Numeric(40, 0),
        nullable=False,
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    owner_id = Column(Numeric(40, 0), nullable=False)
    value = Column(Float, nullable=False, server_default="0")


class DBVivacity(IVivacity):
    def __init__(self, db_instance: DBVivacityModel) -> None:
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
            db_instance: t.Optional[DBVivacityModel] = db.query(DBVivacityModel).filter(DBVivacityModel.id == self.__db_instance.id).first()  # type: ignore

            if db_instance is None:
                return

            self.__db_instance = db_instance
            self.__db_instance.value = new_value
            db.commit()
            db.refresh(self.__db_instance)


class DeletedVivacity(IVivacity, LinkedUniqueObjectMixin):
    def __init__(self, db_instance: DBVivacityModel) -> None:
        super().__init__(id=int(db_instance.id), owner_id=int(db_instance.owner_id))  # type: ignore
        self.__value = float(db_instance.value)  # type: ignore

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, new_value: float) -> None:
        raise ValueError("Can't set value for DeletedVivacity")


class VivacityFactory(IVivacityFactory):
    def __init__(self, di_container: IDependencyInjector) -> None:
        super().__init__()
        id_generator: t.Optional[IUniqueIDGenerator] = di_container.get_singleton(
            IUniqueIDGenerator
        )
        if id_generator == None:
            raise ValueError("Can't get id generator from DI container")

        self.__id_generator: IUniqueIDGenerator = id_generator

    def create(self, owner_id: int) -> IVivacity:
        if self.get(owner_id=owner_id):
            raise ValueError("Vivacity already created")

        with database_session() as db:
            hunger_instance: t.Optional[DBVivacityModel] = (
                db.query(DBVivacityModel)
                .filter(DBVivacityModel.owner_id == owner_id)
                .first()
            )

            if hunger_instance is not None:
                raise ValueError("Chat already created")

            hunger_instance = DBVivacityModel(
                id=self.__id_generator.create_id(),
                owner_id=owner_id,
            )
            db.add(hunger_instance)
            db.commit()
            db.refresh(hunger_instance)

            return DBVivacity(hunger_instance)

    def get(
        self,
        owner_id: t.Optional[int] = None,
        object_id: t.Optional[int] = None,
    ) -> t.Optional[IVivacity]:
        if owner_id is None and object_id is None:
            raise ValueError("Information not provided")

        with database_session() as db:
            db_query = db.query(DBVivacityModel)

            if object_id:
                db_query = db_query.filter(DBVivacityModel.id == object_id)

            if owner_id:
                db_query = db_query.filter(DBVivacityModel.owner_id == owner_id)

            vivacity_instance: t.Optional[DBVivacityModel] = db_query.first()

            if vivacity_instance is None:
                return None

            return DBVivacity(vivacity_instance)

    def delete(self, owner_id: int) -> IVivacity:
        with database_session() as db:
            db_instance: t.Optional[DBVivacityModel] = (
                db.query(DBVivacityModel)
                .filter(DBVivacityModel.owner_id == owner_id)
                .first()
            )

            if db_instance is None:
                raise ValueError("Vivacity not created")

            vivacity: IVivacity = DeletedVivacity(db_instance)

            db_instance.delete()
            db.commit()

            return vivacity


class VivacityEngineComponent(IVivacityEngineComponent, Observable):
    def __init__(self, vivacity_factory: IVivacityFactory) -> None:
        super().__init__()
        self.__vivacity_factory = vivacity_factory

    def create_vivacity(self, owner_id: int) -> IVivacity:
        return self.__vivacity_factory.create(owner_id)

    def create_or_get_vivacity(self, owner_id: int) -> IVivacity:
        vivacity_instance: t.Optional[IVivacity] = self.get_vivacity(owner_id=owner_id)

        if vivacity_instance is not None:
            return vivacity_instance

        vivacity_instance = self.create_vivacity(owner_id)

        return vivacity_instance

    def get_vivacity(
        self,
        owner_id: t.Optional[int] = None,
        object_id: t.Optional[int] = None,
    ) -> t.Optional[IVivacity]:
        return self.__vivacity_factory.get(owner_id, object_id)

    def delete_vivacity(self, owner_id: int) -> IVivacity:
        return self.__vivacity_factory.delete(owner_id)

    def update_state(self, time_delta: float) -> None:
        pass
