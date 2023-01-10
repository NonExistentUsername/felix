import pytest
import typing as t

from felix.core.objects.observer import Observable, IObserver

@pytest.fixture
def test_observable_component() -> Observable:
    return Observable()

class SimpleObserver(IObserver):
    def __init__(self) -> None:
        super().__init__()
        self.last_message: t.Optional[str] = None
        self.call_count: int = 0
    
    def get_last_message(self) -> t.Optional[str]:
        return self.last_message

    def notify(self, message: str) -> None:
        self.last_message = message
        self.call_count += 1

class AutoRemoveObserver(SimpleObserver):
    def __init__(self, observable: Observable) -> None:
        super().__init__()
        self.__observable: Observable = observable
    
    def notify(self, message: str) -> None:
        super().notify(message)
        self.__observable.remove_observer(self)
        

class TestObservable:
    def test_observer(self, test_observable_component: Observable):
        simple_observer = SimpleObserver()
        test_observable_component.add_observer(simple_observer)

        assert simple_observer.call_count == 0
        
        test_observable_component.notify("Example message")
        assert simple_observer.last_message == "Example message"
        assert simple_observer.call_count == 1

        test_observable_component.notify("123!@3#33")
        assert simple_observer.last_message == "123!@3#33"
        assert simple_observer.call_count == 2

        test_observable_component.remove_observer(simple_observer)
        test_observable_component.notify("end -23")
        assert simple_observer.last_message == "123!@3#33"
        assert simple_observer.call_count == 2

        test_observable_component.add_observer(simple_observer)
        test_observable_component.add_observer(simple_observer)
        test_observable_component.notify("end -23")
        assert simple_observer.last_message == "end -23"
        assert simple_observer.call_count == 3

        test_observable_component.add_observer(SimpleObserver())
        test_observable_component.add_observer(SimpleObserver())
        test_observable_component.add_observer(simple_observer)
        test_observable_component.notify("end -23")
        assert simple_observer.last_message == "end -23"
        assert simple_observer.call_count == 4
    
        auto_remove_observer = AutoRemoveObserver(test_observable_component)
        test_observable_component.add_observer(auto_remove_observer)

        assert auto_remove_observer.last_message == None
        assert auto_remove_observer.call_count == 0

        test_observable_component.notify("auto remove test")

        assert simple_observer.last_message == "auto remove test"
        assert simple_observer.call_count == 5
        assert auto_remove_observer.last_message == "auto remove test"
        assert auto_remove_observer.call_count == 1

    
        test_observable_component.notify("auto remove test 2")
        assert simple_observer.last_message == "auto remove test 2"
        assert simple_observer.call_count == 6
        assert auto_remove_observer.last_message == "auto remove test"
        assert auto_remove_observer.call_count == 1
