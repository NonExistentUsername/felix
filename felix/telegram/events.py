from core.tools.observer import IEvent


class BotCommandEvent(IEvent):
    def __init__(self, command: str, **kwargs) -> None:
        super().__init__()

        self.command = command
        self.kwargs = kwargs


class BotCallbackEvent(IEvent):
    def __init__(self, callback_data: str, **kwargs) -> None:
        super().__init__()
        self.callback_data = callback_data
        self.kwargs = kwargs
