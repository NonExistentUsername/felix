from ...core.tools.observer import IEvent

class BotCommandEvent(IEvent):
    def __init__(self, command: str, **kwargs) -> None:
        super().__init__()

        self.command = command
        self.kwargs = kwargs