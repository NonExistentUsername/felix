from core.general.events import ObjectCreated
from core.tools.observer import IEvent

from .interfaces import IPet


class PetCreated(ObjectCreated):
    def __init__(self, instance: IPet) -> None:
        super().__init__(instance)

    def get_instance(self) -> IPet:
        return super().get_instance()
