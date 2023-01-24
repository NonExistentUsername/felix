import typing as t
from datetime import datetime, timedelta
from decimal import Decimal

from core.database import Base, database_session
from core.general.unique_object import IUniqueIDGenerator
from core.tools.dependency_injector import IDependencyInjector
from core.tools.observer import Observable
from sqlalchemy import (
    DECIMAL,
    BigInteger,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Numeric,
    String,
)

from .interfaces import (
    ICollectionMethod,
    IPeriodicMoneyBonusEngineComponent,
    IPeriodicMoneyBonusInfo,
    IPeriodicMoneyBonusInfoFactory,
)


class DBPeriodicMoneyBonusInfoModel(Base):
    __tablename__ = "periodic_money_bonus"

    id = Column(
        Numeric(40, 0),
        nullable=False,
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    owner_id = Column(Numeric(40, 0), nullable=False)
    last_collected_at = Column(DateTime(timezone=True), nullable=True)


class DBPeriodicMoneyBonusInfo(IPeriodicMoneyBonusInfo):
    def __init__(self, db_instance: DBPeriodicMoneyBonusInfoModel) -> None:
        super().__init__()
        self.__db_instance = db_instance

    def get_id(self) -> int:
        return int(self.__db_instance.id)  # type: ignore

    def get_owner_id(self) -> int:
        return int(self.__db_instance.owner_id)  # type: ignore

    @property
    def last_collected_at(self) -> t.Optional[datetime]:
        return datetime(self.__db_instance)  # type: ignore

    @last_collected_at.setter
    def last_collected_at(self, new_value: datetime) -> t.Optional[datetime]:
        with database_session() as db:
            pass


class Collect100CoinsEveryday(ICollectionMethod):
    def can_collect(self, last_collected_at: t.Optional[datetime]) -> bool:
        if not last_collected_at:
            return True

        return last_collected_at.day < datetime.utcnow().day

    def calc(self, last_collected_at: t.Optional[datetime]) -> Decimal:
        return Decimal(100)


class PeriodicDBMoneyBonusInfoFactory(IPeriodicMoneyBonusInfoFactory):
    def __init__(self, di_container: IDependencyInjector) -> None:
        super().__init__()
        id_generator: t.Optional[IUniqueIDGenerator] = di_container.get_singleton(
            IUniqueIDGenerator
        )
        if id_generator == None:
            raise ValueError("Can't get id generator from DI container")

        self.__id_generator: IUniqueIDGenerator = id_generator

    def create(self, owner_id: int) -> IPeriodicMoneyBonusInfo:
        if self.get(owner_id=owner_id):
            raise ValueError("MoneyBonusInfo already created")

        with database_session() as db:
            hunger_instance: t.Optional[DBPeriodicMoneyBonusInfoModel] = (
                db.query(DBPeriodicMoneyBonusInfoModel)
                .filter(DBPeriodicMoneyBonusInfoModel.owner_id == owner_id)
                .first()
            )

            if hunger_instance is not None:
                raise ValueError("Chat already created")

            hunger_instance = DBPeriodicMoneyBonusInfoModel(
                id=self.__id_generator.create_id(),
                owner_id=owner_id,
            )
            db.add(hunger_instance)
            db.commit()
            db.refresh(hunger_instance)

            return DBPeriodicMoneyBonusInfo(hunger_instance)

    def get(self, owner_id: int) -> t.Optional[IPeriodicMoneyBonusInfo]:
        with database_session() as db:
            db_query = db.query(DBPeriodicMoneyBonusInfoModel)

            db_query = db_query.filter(
                DBPeriodicMoneyBonusInfoModel.owner_id == owner_id
            )

            vivacity_instance: t.Optional[
                DBPeriodicMoneyBonusInfoModel
            ] = db_query.first()

            if vivacity_instance is None:
                return None

            return DBPeriodicMoneyBonusInfo(vivacity_instance)


class PeriodicMoneyBonusEngineComponent(IPeriodicMoneyBonusEngineComponent, Observable):
    def __init__(
        self,
        periodic_money_bonus_info_factory: IPeriodicMoneyBonusInfoFactory,
        collection_method: ICollectionMethod,
    ) -> None:
        super().__init__()
        self.__periodic_money_bonus_info_factory = periodic_money_bonus_info_factory
        self.__collection_method = collection_method

    def add_bonuses_for_object(self, owner_id: int) -> None:
        self.__periodic_money_bonus_info_factory.create(owner_id)

    def can_collect(self, owner_id: int) -> bool:
        periodic_money_bonus_info: t.Optional[
            IPeriodicMoneyBonusInfo
        ] = self.__periodic_money_bonus_info_factory.get(owner_id)

        if not periodic_money_bonus_info:
            return False

        return self.__collection_method.can_collect(
            periodic_money_bonus_info.last_collected_at
        )

    def collect(self, owner_id: int) -> Decimal:
        periodic_money_bonus_info: t.Optional[
            IPeriodicMoneyBonusInfo
        ] = self.__periodic_money_bonus_info_factory.get(owner_id)

        if not periodic_money_bonus_info:
            return Decimal(0)

        if not self.can_collect(owner_id):
            return Decimal(0)

        value: Decimal = self.__collection_method.calc(
            periodic_money_bonus_info.last_collected_at
        )

        return value

    def update_state(self, time_delta: float) -> None:
        pass
