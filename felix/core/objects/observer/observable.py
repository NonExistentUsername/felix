import typing as t

from .interfaces import IObservable, IObserver

class Observable(IObservable):
    def __init__(self) -> None:
        super().__init__()
        self.__observers: t.List[IObserver] = []

    def notify(self, message: str) -> None:
        for observer in self.__observers:
            observer.notify(message)

    def add_observer(self, observer: IObserver) -> None:
        if not observer in self.__observers:
            self.__observers.append(observer)

    def remove_observer(self, observer: IObserver) -> None:
        self.__observers.remove(observer)