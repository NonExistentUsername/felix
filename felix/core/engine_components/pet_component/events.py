from ...tools.observer import IEvent
from ...general.events import ObjectCreated
from .interfaces import IPet


class PetCreated(ObjectCreated):
    def __init__(self, instance: IPet) -> None:
        super().__init__(instance)

    def get_instance(self) -> IPet:
        return super().get_instance()
