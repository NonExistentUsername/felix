from abc import ABC, abstractmethod

class IObserver(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def notify(self, *args, **kwargs) -> None:
        pass

class IObservable(IObserver):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def add_observer(self, observer: IObserver) -> None:
        pass

    @abstractmethod
    def remove_observer(self, observer: IObserver) -> None:
        pass