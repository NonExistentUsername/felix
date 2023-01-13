from general.engine import IEngine, EngineRunMixin
from general.unique_object import UUID1, IUniqueIDGenerator
from tools.dependency_injector import IDependencyInjector, DependencyInjector
from engine_components.pet_component import (
    PetEngineComponent,
    IPetEngineComponent,
    ChickenPetFactory,
    DefaultDBPetFactory,
)


class PetsEngine(EngineRunMixin, IEngine):
    def __init__(self) -> None:
        super().__init__(tickrate=20)

        self.__di_conrainer: IDependencyInjector = DependencyInjector()
        uuid1_generator: IUniqueIDGenerator = UUID1()
        self.__di_conrainer.register_singleton(IUniqueIDGenerator, uuid1_generator)

        self.__pet_component = PetEngineComponent(
            DefaultDBPetFactory(self.__di_conrainer, "chicken")
        )
        self.__di_conrainer.register_singleton(
            IPetEngineComponent, self.__pet_component
        )

    def update_state(self, time_delta: float) -> None:
        self.__pet_component.update_state(time_delta)

    def get_di_container(self) -> IDependencyInjector:
        return self.__di_conrainer
