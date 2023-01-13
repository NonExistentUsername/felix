import typing as t
from abc import ABC, abstractmethod

from ..core.tools.observer import IObserver, IEvent
from ..core.tools.dependency_injector import IDependencyInjector


class EngineUpdatesListener(IObserver):
    def __init__(self, engine_di_container: IDependencyInjector) -> None:
        super().__init__()

    def notify(self, event: IEvent) -> None:
        pass
