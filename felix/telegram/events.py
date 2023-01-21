from core.tools.observer import IEvent


class BotCommandEvent(IEvent):
    def __init__(self, command: str, chat_id: int, user_id: int, **kwargs) -> None:
        super().__init__()

        self.command = command
        self.chat_id = chat_id
        self.user_id = user_id
        self.kwargs = kwargs


class BotCallbackEvent(IEvent):
    def __init__(
        self, callback_data: str, chat_id: int, user_id: int, message_id: int, **kwargs
    ) -> None:
        super().__init__()
        self.callback_data = callback_data
        self.chat_id = chat_id
        self.user_id = user_id
        self.message_id = message_id
        self.kwargs = kwargs
