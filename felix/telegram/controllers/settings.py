import typing as t
import os
import logging
from telebot import types as tgt

from controller import IController
from core.tools import IDependencyInjector, IObserver, IEvent
from telegram.handlers.settings import command_observable_component
from telegram import tbot, BotCommandEvent, BotCallbackEvent

from core.engine_components.pet_component import IPetEngineComponent
from core.engine_components.telegram_components.chat_manager import (
    ITelegramChatManager,
    ITelegramChat,
)
from core.engine_components.pet_customization_component import (
    IPetCustomizationEngineComponent,
)
from telegram.messages import txt, get_list_of_languages
from telegram import logger


class SettingsController(IObserver):
    def __init__(self, engine_di_container: IDependencyInjector) -> None:
        super().__init__()

        telegram_chat_manager: t.Optional[
            ITelegramChatManager
        ] = engine_di_container.get_singleton(ITelegramChatManager)

        if telegram_chat_manager is None:
            raise ValueError("Can't get engine component for telegram chats")

        self.__telegram_chat_manager: ITelegramChatManager = telegram_chat_manager

        command_observable_component.add_observer(self)

    def __get_or_create_chat(self, chat_id: int) -> ITelegramChat:
        chat_instance: t.Optional[
            ITelegramChat
        ] = self.__telegram_chat_manager.get_chat(telegram_chat_id=chat_id)

        if chat_instance is not None:
            return chat_instance

        return self.__telegram_chat_manager.create_chat(chat_id)

    def __settings_menu_markup(
        self, tg_chat: ITelegramChat
    ) -> tgt.InlineKeyboardMarkup:
        settings_menu = tgt.InlineKeyboardMarkup()
        settings_menu.add(
            tgt.InlineKeyboardButton(
                txt(tg_chat.language_code, "language_settings"),
                callback_data="open_language_settings",
            )
        )

        return settings_menu

    def __language_settings_menu_markup(
        self, tg_chat: ITelegramChat
    ) -> tgt.InlineKeyboardMarkup:
        language_menu = tgt.InlineKeyboardMarkup(row_width=1)
        buttons = [
            tgt.InlineKeyboardButton(
                txt(language_code, "language_name"),
                callback_data=f"set_language_{language_code}",
            )
            for language_code in get_list_of_languages()
        ]
        buttons.append(
            tgt.InlineKeyboardButton(
                "<< " + txt(tg_chat.language_code, "back"),
                callback_data=f"open_settings",
            )
        )
        language_menu.add(*buttons)

        return language_menu

    def __open_setting_command(self, event: BotCommandEvent) -> None:
        tg_chat: ITelegramChat = self.__get_or_create_chat(event.chat_id)

        tbot.send_message(
            event.chat_id,
            txt(tg_chat.language_code, "settings_menu"),
            reply_markup=self.__settings_menu_markup(tg_chat),
        )

    def __set_language_command(self, event: BotCommandEvent) -> None:
        try:
            language_code: str = str(event.kwargs["language_code"])
        except Exception as e:
            logger.exception(e)
            return

        tg_chat: ITelegramChat = self.__get_or_create_chat(event.chat_id)

        tg_chat.language_code = language_code

        tbot.send_message(event.chat_id, txt(tg_chat.language_code, "language_set"))

    def __open_language_settings_callback(self, event: BotCallbackEvent) -> None:
        tg_chat: ITelegramChat = self.__get_or_create_chat(event.chat_id)

        tbot.edit_message_text(
            txt(tg_chat.language_code, "set_language"),
            event.chat_id,
            event.message_id,
            reply_markup=self.__language_settings_menu_markup(tg_chat),
        )

    def __open_settings_callback(self, event: BotCallbackEvent) -> None:
        tg_chat: ITelegramChat = self.__get_or_create_chat(event.chat_id)

        tbot.edit_message_text(
            txt(tg_chat.language_code, "settings_menu"),
            event.chat_id,
            event.message_id,
            reply_markup=self.__settings_menu_markup(tg_chat),
        )

    def __notify_command(self, event: BotCommandEvent) -> None:
        if event.command == "open_settings":
            self.__open_setting_command(event)
        elif event.command == "set_language":
            self.__set_language_command(event)

    def __notify_callback(self, event: BotCallbackEvent) -> None:
        if event.callback_data == "open_language_settings":
            self.__open_language_settings_callback(event)
        elif event.callback_data == "open_settings":
            self.__open_settings_callback(event)

    def notify(self, event: t.Union[BotCommandEvent, BotCallbackEvent]) -> None:
        if isinstance(event, BotCommandEvent):
            self.__notify_command(event)
        elif isinstance(event, BotCallbackEvent):
            self.__notify_callback(event)
