import typing as t
from .interfaces import IDependencyInjector

class DependencyInjector(IDependencyInjector):
    def __init__(self) -> None:
        super().__init__()
        self.__singletons = {}

    def register_singleton(self, interface_type: type, object) -> None:
        if not isinstance(interface_type, type):
            raise ValueError(f"{interface_type} is not a type.")
        
        if not isinstance(object, interface_type):
            raise ValueError(f"object is not instance of {interface_type}.")
        
        self.__singletons[interface_type] = object

    def get_singleton(self, interface_type: type) -> t.Any:
        if interface_type in self.__singletons:
            return self.__singletons[interface_type]
        
        return None