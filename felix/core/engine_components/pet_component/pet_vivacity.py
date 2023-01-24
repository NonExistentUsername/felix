from core.engine_components.pet_component import PetCreated, PetDeleted
from core.engine_components.vivacity_component.interfaces import (
    IVivacityEngineComponent,
)
from core.tools.observer import IEvent, IObserver


class PetVivacityAutoCreation(IObserver):
    def __init__(self, vivacity_engine_component: IVivacityEngineComponent) -> None:
        super().__init__()
        self.__vivacity_engine_component = vivacity_engine_component

    def notify(self, event: IEvent) -> None:
        if isinstance(event, PetCreated):
            self.__vivacity_engine_component.create_vivacity(
                owner_id=event.get_instance().get_id()
            )
        elif isinstance(event, PetDeleted):
            self.__vivacity_engine_component.delete_vivacity(
                owner_id=event.get_instance().get_id()
            )
