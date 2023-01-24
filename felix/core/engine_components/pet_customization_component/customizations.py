import typing as t

from core.database import Base, database_session
from core.general.unique_object import IUniqueIDGenerator, LinkedUniqueObjectMixin
from core.tools.dependency_injector import IDependencyInjector
from core.tools.observer import IEvent, IObserver, Observable
from sqlalchemy import DECIMAL, BigInteger, Column, ForeignKey, Numeric, String

from .events import NameChanged
from .interfaces import (
    IPetCustomization,
    IPetCustomizationEngineComponent,
    IPetCustomizationFactory,
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

    def get_owner_id(self) -> int:
        return int(self.__instance.owner_id)  # type: ignore

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


class DeletedPetCustomization(IPetCustomization, LinkedUniqueObjectMixin):
    def __init__(self, db_instance: DBPetCustomizationModel) -> None:
        super().__init__(id=int(db_instance.id), owner_id=int(db_instance.owner_id))  # type: ignore
        self.__name = str(db_instance.name)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, new_name: str) -> None:
        raise ValueError("Can't set name for DeletedPetCustomization")


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

    def delete(self, pet_id: int) -> IPetCustomization:
        with database_session() as db:
            db_instance: t.Optional[DBPetCustomizationModel] = (
                db.query(DBPetCustomizationModel)
                .filter(DBPetCustomizationModel.owner_id == pet_id)
                .first()
            )

            if db_instance is None:
                raise ValueError("PetCustomization not created")

            pet_customization: IPetCustomization = DeletedPetCustomization(db_instance)

            db_instance.delete()
            db.commit()

            return pet_customization


class ObservableCustomization(IPetCustomization, Observable):
    def __init__(
        self,
        customization_instance: IPetCustomization,
    ) -> None:
        super().__init__()
        self.__customization_instance = customization_instance

    def get_id(self) -> int:
        return self.__customization_instance.get_id()

    def get_owner_id(self) -> int:
        return self.__customization_instance.get_owner_id()

    @property
    def name(self) -> str:
        return self.__customization_instance.name

    @name.setter
    def name(self, new_name: str) -> None:
        self.__customization_instance.name = new_name
        self.notify(NameChanged(new_name, self))


class PetCustomizationEngineComponent(
    IPetCustomizationEngineComponent, Observable, IObserver
):
    def __init__(self, pet_customization_factory: IPetCustomizationFactory) -> None:
        super().__init__()
        self.__pet_customization_factory = pet_customization_factory

    def get_pet_customization(self, pet_id: int) -> IPetCustomization:
        instance: t.Optional[IPetCustomization] = self.__pet_customization_factory.get(
            pet_id
        )

        if instance is None:
            instance = self.__pet_customization_factory.create(pet_id)

        instance = ObservableCustomization(instance)
        instance.add_observer(self)

        return instance

    def delete_pet_customization(self, pet_id: int) -> IPetCustomization:
        return self.__pet_customization_factory.delete(pet_id)

    def update_state(self, time_delta: float) -> None:
        pass
