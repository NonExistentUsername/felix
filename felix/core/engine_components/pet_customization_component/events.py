from core.tools.observer import IEvent

from .interfaces import IPetCustomization


class NameChanged(IEvent):
    def __init__(
        self, new_name: str, pet_customization_instance: IPetCustomization
    ) -> None:
        super().__init__()
        self.new_name = new_name
        self.pet_customization_instance = pet_customization_instance
