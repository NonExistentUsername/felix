import typing as t
from sqlalchemy import Column, String, ForeignKey, BigInteger, Numeric, DECIMAL

from core.tools.dependency_injector import IDependencyInjector
from core.tools.observer import Observable
from core.general.unique_object import IUniqueIDGenerator
from core.database import Base
from core.database import Base, database_session

from .interfaces import (
    IPetCustomization,
    IPetCustomizationFactory,
    IPetCustomizationEngineComponent,
)


class DBPetCustomizationModel(Base):
    __tablename__ = "pets_customization"

    id = Column(
        Numeric(40, 0),
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=False,
    )
    owner_id = Column(Numeric(40, 0), nullable=False)
    name = Column(String(63))


class DBPetCustomization(IPetCustomization):
    def __init__(self, instance: DBPetCustomizationModel) -> None:
        super().__init__()
        self.__instance: DBPetCustomizationModel = instance

    def get_id(self) -> int:
        return int(self.__instance.id)  # type: ignore

    @property
    def name(self) -> str:
        return str(self.__instance.name)

    @name.setter
    def name(self, new_name: str) -> None:
        if len(new_name) == 0:
            raise ValueError("Can't set empty pet name")

        if len(new_name) > 63:
            raise ValueError("Pet name cannot be longer than 63 characters")

        with database_session() as db:
            instance: t.Optional[DBPetCustomizationModel] = (
                db.query(DBPetCustomizationModel)
                .filter(DBPetCustomizationModel.id == self.__instance.id)
                .first()
            )

            if instance is None:
                return

            self.__instance = instance
            self.__instance.name = new_name  # type: ignore
            db.commit()
            db.refresh(self.__instance)


class PetCustomizationFactory(IPetCustomizationFactory):
    def __init__(self, di_container: IDependencyInjector, default_name: str) -> None:
        super().__init__()
        id_generator: t.Optional[IUniqueIDGenerator] = di_container.get_singleton(
            IUniqueIDGenerator
        )
        if id_generator == None:
            raise ValueError("Can't get id generator from DI container")

        self.__id_generator: IUniqueIDGenerator = id_generator
        self.__deafult_name = default_name

    def get(self, pet_id: int) -> t.Optional[IPetCustomization]:
        with database_session() as db:
            instance: t.Optional[DBPetCustomizationModel] = (
                db.query(DBPetCustomizationModel)
                .filter(DBPetCustomizationModel.owner_id == pet_id)
                .first()
            )

            if instance is None:
                return None

            return DBPetCustomization(instance)

    def create(self, pet_id: int) -> IPetCustomization:
        with database_session() as db:
            instance: DBPetCustomizationModel = DBPetCustomizationModel(
                id=self.__id_generator.create_id(),
                owner_id=pet_id,
                name=self.__deafult_name,
            )
            db.add(instance)
            db.commit()
            db.refresh(instance)
            return DBPetCustomization(instance)


class PetCustomizationEngineComponent(IPetCustomizationEngineComponent, Observable):
    def __init__(self, pet_customization_factory: IPetCustomizationFactory) -> None:
        super().__init__()
        self.__pet_customization_factory = pet_customization_factory

    def get_pet_customization(self, pet_id: int) -> IPetCustomization:
        instance: t.Optional[IPetCustomization] = self.__pet_customization_factory.get(
            pet_id
        )

        if instance is None:
            instance = self.__pet_customization_factory.create(pet_id)

        return instance

    def update_state(self, time_delta: float) -> None:
        pass
