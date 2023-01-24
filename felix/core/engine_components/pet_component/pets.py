import typing as t

from core.database import Base, database_session
from core.general.unique_object import IUniqueIDGenerator, LinkedUniqueObjectMixin
from core.tools import IDependencyInjector, Observable
from sqlalchemy import DECIMAL, BigInteger, Column, ForeignKey, Numeric, String

from .events import PetCreated, PetDeleted
from .interfaces import IPet, IPetEngineComponent, IPetFactory


class DBPetModel(Base):
    __tablename__ = "pets"

    id = Column(
        Numeric(40, 0),
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=False,
    )
    owner_id = Column(Numeric(40, 0), nullable=False)
    type = Column(String(63))


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


class DeletedPet(IPet, LinkedUniqueObjectMixin):
    def __init__(self, instance: DBPetModel) -> None:
        super().__init__(id=int(instance.id), owner_id=int(instance.owner_id))  # type: ignore
        self.__type = str(instance.type)

    @property
    def type(self) -> str:
        return self.__type


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

    def get(
        self,
        owner_id: t.Optional[int] = None,
        pet_id: t.Optional[int] = None,
    ) -> t.Optional[IPet]:

        with database_session() as db:
            db_query = db.query(DBPetModel)

            if owner_id:
                db_query = db_query.filter(DBPetModel.owner_id == owner_id)

            if pet_id:
                db_query = db_query.filter(DBPetModel.id == pet_id)

            chat_instance: t.Optional[DBPetModel] = db_query.first()

            if chat_instance is None:
                return None

            return DBPet(chat_instance)

    def delete_pet(self, owner_id: int) -> IPet:
        with database_session() as db:
            instance: t.Optional[DBPetModel] = (
                db.query(DBPetModel).filter(DBPetModel.owner_id == owner_id).first()
            )

            if not instance:
                raise ValueError("Pet not created")

            pet: IPet = DeletedPet(instance)

            instance.delete()
            db.commit()

            return pet


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

        pet_instance = self.__pet_factory.create(owner_id)
        self.notify(PetCreated(pet_instance))

        return pet_instance

    def get_pet(
        self,
        owner_id: t.Optional[int] = None,
        pet_id: t.Optional[int] = None,
    ) -> t.Optional[IPet]:
        return self.__pet_factory.get(owner_id=owner_id, pet_id=pet_id)

    def update_state(self, time_delta: float) -> None:
        pass

    def delete_pet(self, owner_id: int) -> None:
        pet: IPet = self.__pet_factory.delete_pet(owner_id)
        self.notify(PetDeleted(pet))
