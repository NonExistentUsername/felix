import logging
import os

from .engine_components.economy_component import (
    BalanceFactory,
    EconomyEngineComponent,
    IEconomyEngineComponent,
)
from .engine_components.hunger_component import (
    HungerEngineComponent,
    HungerFactory,
    IHungerEngineComponent,
)
from .engine_components.pet_component import (
    ChickenPetFactory,
    DefaultDBPetFactory,
    IPetEngineComponent,
    PetBalanceAutoCreation,
    PetEngineComponent,
    PetHungerAutoCreation,
    PetVivacityAutoCreation,
)
from .engine_components.pet_customization_component import (
    IPetCustomizationEngineComponent,
    PetCustomizationEngineComponent,
    PetCustomizationFactory,
)
from .engine_components.telegram_components.chat_manager import (
    ITelegramChatManager,
    TelegramChatManager,
)
from .engine_components.vivacity_component import (
    IVivacityEngineComponent,
    VivacityEngineComponent,
    VivacityFactory,
)
from .general.engine import EngineRunMixin, IEngine
from .general.unique_object import UUID1, IUniqueIDGenerator
from .tools.dependency_injector import DependencyInjector, IDependencyInjector


class PetsEngine(EngineRunMixin, IEngine):
    def __create_logger(self) -> logging.Logger:
        logger = logging.Logger("PetsLogging")

        DEBUG = os.getenv("DEBUG") == "True"

        if DEBUG:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        return logger

    def __init__(self) -> None:
        super().__init__(tickrate=20)

        self.__di_conrainer: IDependencyInjector = DependencyInjector()
        uuid1_generator: IUniqueIDGenerator = UUID1()
        self.__di_conrainer.register_singleton(IUniqueIDGenerator, uuid1_generator)

        self.__pet_component = PetEngineComponent(
            DefaultDBPetFactory(self.__di_conrainer, "cat")
        )
        self.__di_conrainer.register_singleton(
            IPetEngineComponent, self.__pet_component
        )
        self.__pet_customization_component = PetCustomizationEngineComponent(
            PetCustomizationFactory(self.__di_conrainer, "Name")
        )
        self.__di_conrainer.register_singleton(
            IPetCustomizationEngineComponent, self.__pet_customization_component
        )
        self.__di_conrainer.register_singleton(
            ITelegramChatManager, TelegramChatManager(self.__di_conrainer)
        )
        self.__hunger_engine_component: IHungerEngineComponent = HungerEngineComponent(
            HungerFactory(self.__di_conrainer)
        )
        self.__di_conrainer.register_singleton(
            IHungerEngineComponent,
            self.__hunger_engine_component,
        )
        pet_hunger_auto_creation = PetHungerAutoCreation(self.__hunger_engine_component)
        self.__pet_component.add_observer(pet_hunger_auto_creation)
        self.__vivacity_engine_component = VivacityEngineComponent(
            VivacityFactory(self.__di_conrainer)
        )
        vivacity_engine_component = PetVivacityAutoCreation(
            self.__vivacity_engine_component
        )
        self.__pet_component.add_observer(vivacity_engine_component)
        self.__di_conrainer.register_singleton(
            IVivacityEngineComponent,
            self.__vivacity_engine_component,
        )
        self.__economy_engine_component: IEconomyEngineComponent = (
            EconomyEngineComponent(BalanceFactory(self.__di_conrainer))
        )
        pet_balance_auto_creation = PetBalanceAutoCreation(
            self.__economy_engine_component
        )
        self.__pet_component.add_observer(pet_balance_auto_creation)
        self.__di_conrainer.register_singleton(
            IEconomyEngineComponent, self.__economy_engine_component
        )
        self.__di_conrainer.register_singleton(logging.Logger, self.__create_logger())

    def update_state(self, time_delta: float) -> None:
        self.__pet_component.update_state(time_delta)

    def get_di_container(self) -> IDependencyInjector:
        return self.__di_conrainer
