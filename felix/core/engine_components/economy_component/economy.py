import typing as t
from decimal import Context, Decimal

from core.database import Base, database_session
from core.general.unique_object import IUniqueIDGenerator, LinkedUniqueObjectMixin
from core.tools.dependency_injector import IDependencyInjector
from core.tools.observer import Observable
from sqlalchemy import DECIMAL, BigInteger, Column, Float, ForeignKey, Numeric, String

from .interfaces import IBalance, IBalanceFactory, IEconomyEngineComponent


class DBBalanceModel(Base):
    __tablename__ = "balance"

    id = Column(
        Numeric(40, 0),
        nullable=False,
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    owner_id = Column(Numeric(40, 0), nullable=False)
    value = Column(Numeric(20, 0), nullable=False, server_default="0")


class DBBalance(IBalance):
    def __init__(self, db_instance: DBBalanceModel) -> None:
        super().__init__()
        self.__db_instance = db_instance

    def get_id(self) -> int:
        return int(self.__db_instance.id)  # type: ignore

    def get_owner_id(self) -> int:
        return int(self.__db_instance.owner_id)  # type: ignore

    @property
    def value(self) -> Decimal:
        return Decimal(self.__db_instance.value, Context(prec=3))  # type: ignore

    @value.setter
    def value(self, new_value: Decimal) -> None:
        with database_session() as db:
            db_instance: t.Optional[DBBalanceModel] = (
                db.query(DBBalanceModel)
                .filter(DBBalanceModel.id == self.__db_instance.id)
                .first()
            )

            if db_instance is None:
                return

            self.__db_instance = db_instance
            self.__db_instance.value = new_value
            db.commit()
            db.refresh(self.__db_instance)


class DeletedBalance(IBalance, LinkedUniqueObjectMixin):
    def __init__(self, db_instance: DBBalanceModel) -> None:
        super().__init__(
            id=int(db_instance.id), owner_id=int(db_instance.owner_id)  # type: ignore
        )
        self.__value = Decimal(db_instance.value)  # type: ignore

    @property
    def value(self) -> Decimal:
        return self.__value

    @value.setter
    def value(self, new_value: Decimal) -> None:
        raise ValueError("Can't set value for DeletedBalance")


class BalanceFactory(IBalanceFactory):
    def __init__(self, di_container: IDependencyInjector) -> None:
        super().__init__()
        id_generator: t.Optional[IUniqueIDGenerator] = di_container.get_singleton(
            IUniqueIDGenerator
        )
        if id_generator == None:
            raise ValueError("Can't get id generator from DI container")

        self.__id_generator: IUniqueIDGenerator = id_generator

    def create(self, owner_id: int) -> IBalance:
        if self.get(owner_id=owner_id):
            raise ValueError("Balance already created")

        with database_session() as db:
            balance_instance = DBBalanceModel(
                id=self.__id_generator.create_id(),
                owner_id=owner_id,
            )
            db.add(balance_instance)
            db.commit()
            db.refresh(balance_instance)

            return DBBalance(balance_instance)

    def get(
        self,
        owner_id: t.Optional[int] = None,
        object_id: t.Optional[int] = None,
    ) -> t.Optional[IBalance]:
        if owner_id is None and object_id is None:
            raise ValueError("Information not provided")

        with database_session() as db:
            db_query = db.query(DBBalanceModel)

            if object_id:
                db_query = db_query.filter(DBBalanceModel.id == object_id)

            if owner_id:
                db_query = db_query.filter(DBBalanceModel.owner_id == owner_id)

            balance_instance: t.Optional[DBBalanceModel] = db_query.first()

            if balance_instance is None:
                return None

            return DBBalance(balance_instance)

    def delete(self, owner_id: int) -> IBalance:
        with database_session() as db:
            db_instance: t.Optional[DBBalanceModel] = (
                db.query(DBBalanceModel)
                .filter(DBBalanceModel.owner_id == owner_id)
                .first()
            )

            if db_instance is None:
                raise ValueError("Balance not created")

            balance: IBalance = DeletedBalance(db_instance)

            db_instance.delete()
            db.commit()

            return balance


class EconomyEngineComponent(IEconomyEngineComponent, Observable):
    def __init__(self, balance_factory: IBalanceFactory) -> None:
        super().__init__()
        self.__balance_factory = balance_factory

    def create_balance(self, owner_id: int) -> IBalance:
        return self.__balance_factory.create(owner_id)

    def create_or_get_balance(self, owner_id: int) -> IBalance:
        balance: t.Optional[IBalance] = self.get_balance(owner_id=owner_id)
        if balance:
            return balance

        return self.create_balance(owner_id)

    def get_balance(
        self,
        owner_id: t.Optional[int] = None,
        object_id: t.Optional[int] = None,
    ) -> t.Optional[IBalance]:
        return self.__balance_factory.get(owner_id=owner_id, object_id=object_id)

    def delete_balance(self, owner_id: int) -> IBalance:
        return self.__balance_factory.delete(owner_id)

    def update_state(self, time_delta: float) -> None:
        pass
