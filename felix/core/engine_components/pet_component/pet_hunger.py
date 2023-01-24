from core.engine_components.hunger_component.interfaces import IHungerEngineComponent
from core.engine_components.pet_component import PetCreated, PetDeleted
from core.tools.observer import IEvent, IObserver


class PetHungerAutoCreation(IObserver):
    def __init__(self, hunger_engine_component: IHungerEngineComponent) -> None:
        super().__init__()
        self.__hunger_engine_component = hunger_engine_component

    def notify(self, event: IEvent) -> None:
        if isinstance(event, PetCreated):
            self.__hunger_engine_component.create_hunger(
                owner_id=event.get_instance().get_id()
            )
        elif isinstance(event, PetDeleted):
            self.__hunger_engine_component.delete_hunger(
                owner_id=event.get_instance().get_id()
            )
