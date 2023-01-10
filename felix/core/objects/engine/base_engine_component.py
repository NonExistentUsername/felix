from .interfaces import IEngineComponent

class BaseEngineComponent(IEngineComponent):
    def __init__(self) -> None:
        super().__init__()
    
    