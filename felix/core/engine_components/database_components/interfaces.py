from objects.engine import IEngineComponent

class IDatabaseEngineComponent(IEngineComponent):
    def __init__(self) -> None:
        super().__init__()
        