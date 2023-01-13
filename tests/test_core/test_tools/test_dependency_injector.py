import pytest
import typing as t
from abc import ABC, abstractmethod

from felix.core.tools.dependency_injector import DependencyInjector


@pytest.fixture
def test_di() -> DependencyInjector:
    return DependencyInjector()


class SimpleInterface(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def test(self) -> int:
        pass


class SimpleInterfaceRealisation(SimpleInterface):
    def __init__(self) -> None:
        super().__init__()
        self.number = 42

    def test(self) -> int:
        return self.number


class SimpleRandomClass:
    def test(self) -> int:
        return 12


class TestDependencyInjector:
    def test_di(self, test_di: DependencyInjector):
        sir = SimpleInterfaceRealisation()

        test_di.register_singleton(SimpleInterface, sir)
        g_sir: SimpleInterfaceRealisation = test_di.get_singleton(SimpleInterface)

        assert g_sir.test() == 42

        g_sir.number = 3

        assert g_sir.test() == 3
        assert g_sir.test() == sir.test()
        assert g_sir == sir

        sir2 = SimpleInterfaceRealisation()

        test_di.register_singleton(SimpleInterface, sir2)
        g_sir2: SimpleInterfaceRealisation = test_di.get_singleton(SimpleInterface)

        assert g_sir2.test() == 42

        sir2.number = 23

        assert g_sir2.test() == 23
        assert g_sir2.test() == sir2.test()
        assert g_sir2 == sir2
        assert g_sir != g_sir2
