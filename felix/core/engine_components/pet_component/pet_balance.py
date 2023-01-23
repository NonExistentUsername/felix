from core.engine_components.economy_component.interfaces import IEconomyEngineComponent
from core.engine_components.pet_component import PetCreated
from core.tools.observer import IEvent, IObserver


class PetBalanceAutoCreation(IObserver):
    def __init__(self, economy_engine_component: IEconomyEngineComponent) -> None:
        super().__init__()
        self.__economy_engine_component = economy_engine_component

    def notify(self, event: IEvent) -> None:
        if isinstance(event, PetCreated):
            self.__economy_engine_component.create_balance(
                owner_id=event.get_instance().get_id()
            )
