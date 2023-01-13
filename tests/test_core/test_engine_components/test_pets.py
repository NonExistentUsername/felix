import pytest
from felix.core.engine_components.pet_component import (
    IPet,
    Pet,
    PetEngineComponent,
    ChickenPetFactory,
    DefaultPetFactory,
    DefaultPetFactoryBase,
    DefaultDBPetFactory,
)
from felix.core.tools.dependency_injector import DependencyInjector
from felix.core.general.unique_object import IUniqueIDGenerator


@pytest.fixture
def test_pet() -> Pet:
    return Pet(2, 1, "test")


class SimpleUniqueIDGenerator(IUniqueIDGenerator):
    def __init__(self) -> None:
        super().__init__()
        self.__counter = 0

    def create_id(self) -> int:
        self.__counter += 1
        return self.__counter


simple_unique_id_generator = SimpleUniqueIDGenerator()
di_container = DependencyInjector()

di_container.register_singleton(IUniqueIDGenerator, simple_unique_id_generator)


@pytest.fixture
def test_chicken_pet_factory() -> ChickenPetFactory:
    return ChickenPetFactory(di_container)


@pytest.fixture
def test_pet_engine_component() -> PetEngineComponent:
    return PetEngineComponent(ChickenPetFactory(di_container))


@pytest.fixture
def test_default_pet_factory() -> DefaultPetFactory:
    return DefaultPetFactory(di_container, "default")


class TestPet:
    def test_pet(self, test_pet: Pet) -> None:
        pass


class TestPetFactory:
    def test_chicken_pet_factory(
        self, test_chicken_pet_factory: ChickenPetFactory
    ) -> None:
        with pytest.raises(ValueError):
            ChickenPetFactory(DependencyInjector())

        pet: IPet = test_chicken_pet_factory.create(918)

        assert pet.type == "chicken"
        assert pet.get_owner_id() == 918
        assert pet.get_owner_id() == 918

        pet: IPet = test_chicken_pet_factory.create(33919)

        assert pet.type == "chicken"
        assert pet.get_owner_id() == 33919
        assert pet.get_owner_id() == 33919

    def test_base_pet_factory(
        self, test_default_pet_factory: DefaultPetFactory
    ) -> None:
        with pytest.raises(ValueError):
            DefaultPetFactory(DependencyInjector(), "default")

        pet: IPet = test_default_pet_factory.create(918)

        assert pet.get_owner_id() == 918
        assert pet.get_owner_id() == 918

        pet: IPet = test_default_pet_factory.create(33919)

        assert pet.get_owner_id() == 33919
        assert pet.get_owner_id() == 33919


class TestPetEngineComponent:
    def test_pet_engine_component(
        self, test_pet_engine_component: PetEngineComponent
    ) -> None:
        pet: IPet = test_pet_engine_component.create_pet(38)

        assert pet.type == "chicken"
        assert pet.get_owner_id() == 38
        assert pet.get_owner_id() == 38

        pet: IPet = test_pet_engine_component.create_pet(13)

        assert pet.type == "chicken"
        assert pet.get_owner_id() == 13
        assert pet.get_owner_id() == 13
