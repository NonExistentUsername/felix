import pytest
import random
import string
import typing as t

from felix.core.objects.observer import Observable, IObserver, IEvent

@pytest.fixture
def test_observable_component() -> Observable:
    return Observable()

class MessageEvent(IEvent):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text: str = text

class SimpleObserver(IObserver):
    def __init__(self) -> None:
        super().__init__()
        self.last_event: t.Optional[MessageEvent] = None
        self.call_count: int = 0
    
    def notify(self, event: IEvent) -> None:
        if not isinstance(event, MessageEvent):
            return

        self.last_event = event
        self.call_count += 1


class AutoRemoveObserver(SimpleObserver):
    def __init__(self, observable: Observable) -> None:
        super().__init__()
        self.__observable: Observable = observable
    
    def notify(self, event: IEvent) -> None:
        super().notify(event)
        self.__observable.remove_observer(self)
        

class TestObservable:
    def __create_random_string(self, min_size: int, max_size: int) -> str:
        size: int = random.randint(min_size, max_size)

        return ''.join(random.choice(string.ascii_letters) for i in range(size))

    def __test_event(self, test_observable_component: Observable, observer: SimpleObserver, is_subscribed: bool) -> None:
        call_count = observer.call_count
        last_event = observer.last_event

        new_call_count = call_count + 1
        new_event = MessageEvent(self.__create_random_string(4, 32))
        test_observable_component.notify(new_event)

        if not is_subscribed:
            assert observer.call_count == call_count
            assert observer.last_event == last_event
        else:
            assert observer.call_count == new_call_count
            assert observer.last_event == new_event


    def test_observer(self, test_observable_component: Observable):
        simple_observer = SimpleObserver()
        test_observable_component.add_observer(simple_observer)

        assert simple_observer.call_count == 0
        assert simple_observer.last_event == None

        self.__test_event(test_observable_component, simple_observer, True)
        self.__test_event(test_observable_component, simple_observer, True)

        test_observable_component.remove_observer(simple_observer)
        
        self.__test_event(test_observable_component, simple_observer, False)
        self.__test_event(test_observable_component, simple_observer, False)

        test_observable_component.add_observer(simple_observer)
        test_observable_component.add_observer(simple_observer)
        
        self.__test_event(test_observable_component, simple_observer, True)
        self.__test_event(test_observable_component, simple_observer, True)

        test_observable_component.add_observer(SimpleObserver())
        test_observable_component.add_observer(SimpleObserver())
        test_observable_component.add_observer(simple_observer)
        
        self.__test_event(test_observable_component, simple_observer, True)
        self.__test_event(test_observable_component, simple_observer, True)

        auto_remove_observer = AutoRemoveObserver(test_observable_component)
        test_observable_component.add_observer(auto_remove_observer)

        assert auto_remove_observer.last_event == None
        assert auto_remove_observer.call_count == 0

        self.__test_event(test_observable_component, auto_remove_observer, True)
        self.__test_event(test_observable_component, auto_remove_observer, False)
        self.__test_event(test_observable_component, auto_remove_observer, False)
        self.__test_event(test_observable_component, simple_observer, True)
        self.__test_event(test_observable_component, simple_observer, True)
