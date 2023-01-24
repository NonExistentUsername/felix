from core.engine_components.periodic_money_bonus import (
    IPeriodicMoneyBonusEngineComponent,
)
from core.engine_components.pet_component import PetCreated
from core.tools.observer import IEvent, IObserver


class PetPeriodicMoneyBonusAutoCreation(IObserver):
    def __init__(
        self, economy_engine_component: IPeriodicMoneyBonusEngineComponent
    ) -> None:
        super().__init__()
        self.__economy_engine_component = economy_engine_component

    def notify(self, event: IEvent) -> None:
        if isinstance(event, PetCreated):
            self.__economy_engine_component.add_bonuses_for_object(
                owner_id=event.get_instance().get_id()
            )
