import typing as t
from sqlalchemy import Column, String, Integer, ForeignKey

from .interfaces import IPet, IPetFactory, IPetEngineComponent
from ...database import Base
from ...database import Base, database_session

from ...general.unique_object import LinkedUniqueObjectMixin, IUniqueIDGenerator
from ...tools import Observable, IDependencyInjector


class DBPetModel(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, index=True)
    type = Column(String)


class Pet(IPet, LinkedUniqueObjectMixin):
    def __init__(self, id: int, owner_id: int, type: str) -> None:
        super().__init__(id=id, owner_id=owner_id)
        self.__type = type

    @property
    def type(self) -> str:
        return self.__type


class DBPet(IPet, LinkedUniqueObjectMixin):
    def __init__(self, instance: DBPetModel) -> None:
        super().__init__(id=int(instance.id), owner_id=int(instance.owner_id))  # type: ignore
        self.__db_instance = instance

    @property
    def type(self) -> str:
        return str(self.__db_instance.type)


class DefaultPetFactoryBase(IPetFactory):
    def __init__(self, di_container: IDependencyInjector, default_type: str) -> None:
        super().__init__()
        id_generator: t.Optional[IUniqueIDGenerator] = di_container.get_singleton(
            IUniqueIDGenerator
        )
        if id_generator == None:
            raise ValueError("Can't get id generator from DI container")

        self._id_generator: IUniqueIDGenerator = id_generator
        self._default_type: str = default_type


class DefaultPetFactory(DefaultPetFactoryBase):
    def __init__(self, di_container: IDependencyInjector, default_type: str) -> None:
        super().__init__(di_container, default_type)

    def create(self, owner_id: int) -> IPet:
        return Pet(self._id_generator.create_id(), owner_id, self._default_type)


class DefaultDBPetFactory(DefaultPetFactoryBase):
    def __init__(self, di_container: IDependencyInjector, default_type: str) -> None:
        super().__init__(di_container, default_type)

    def create(self, owner_id: int) -> IPet:
        if self.get(owner_id) is not None:
            raise ValueError("Pet for this object is already created")

        with database_session() as db:
            pet_instance = DBPetModel(
                id=self._id_generator.create_id(),
                owner_id=owner_id,
                type=self._default_type,
            )
            db.add(pet_instance)
            db.commit()
            db.refresh(pet_instance)

            return DBPet(pet_instance)

    def get(self, owner_id: int) -> t.Optional[IPet]:
        with database_session() as db:
            pet_instance = (
                db.query(DBPetModel).filter(DBPetModel.owner_id == owner_id).first()
            )

            if pet_instance is None:
                return None

            return DBPet(pet_instance)


class ChickenPetFactory(DefaultPetFactory):
    def __init__(self, di_container: IDependencyInjector) -> None:
        super().__init__(di_container, "chicken")


class PetEngineComponent(IPetEngineComponent, Observable):
    def __init__(self, pet_factory: IPetFactory) -> None:
        super().__init__()
        self.__pet_factory = pet_factory

    def create_pet(self, owner_id: int) -> IPet:
        if self.get_pet(owner_id) is not None:
            raise ValueError("Pet for this object is already created")

        return self.__pet_factory.create(owner_id)

    def get_pet(self, owner_id: int) -> t.Optional[IPet]:
        return self.__pet_factory.get(owner_id)

    def update_state(self, time_delta: float) -> None:
        pass
