import logging
import os
import typing as t
from decimal import Decimal

from controller import IController
from core.engine_components.economy_component import IBalance, IEconomyEngineComponent
from core.engine_components.hunger_component import IHunger, IHungerEngineComponent
from core.engine_components.periodic_money_bonus import (
    IPeriodicMoneyBonusEngineComponent,
    IPeriodicMoneyBonusInfo,
)
from core.engine_components.pet_component import IPet, IPetEngineComponent
from core.engine_components.pet_customization_component import (
    IPetCustomization,
    IPetCustomizationEngineComponent,
)
from core.engine_components.telegram_components.chat_manager import (
    ITelegramChat,
    ITelegramChatManager,
)
from core.tools import IDependencyInjector, IEvent, IObserver
from telebot import types as tgt
from telegram import BotCallbackEvent, BotCommandEvent, tbot
from telegram.handlers.economy import command_observable_component
from telegram.messages import txt


class EconomyController(IObserver):
    def __init__(self, di_container: IDependencyInjector) -> None:
        super().__init__()

        telegram_chat_manager: t.Optional[
            ITelegramChatManager
        ] = di_container.get_singleton(ITelegramChatManager)

        if telegram_chat_manager is None:
            raise ValueError("Can't get engine component for telegram chats")

        self.__telegram_chat_manager: ITelegramChatManager = telegram_chat_manager

        balance_engine_component: t.Optional[
            IEconomyEngineComponent
        ] = di_container.get_singleton(IEconomyEngineComponent)

        if balance_engine_component is None:
            raise ValueError("Can't get engine component for economy")

        self.__balance_engine_component: IEconomyEngineComponent = (
            balance_engine_component
        )

        pet_engine_component: t.Optional[
            IPetEngineComponent
        ] = di_container.get_singleton(IPetEngineComponent)

        if pet_engine_component is None:
            raise ValueError("Can't get engine component for pets")

        self.__pet_engine_component: IPetEngineComponent = pet_engine_component

        self.__periodic_money_bonus_engine_component: t.Optional[
            IPeriodicMoneyBonusEngineComponent
        ] = di_container.get_singleton(IPeriodicMoneyBonusEngineComponent)

        command_observable_component.add_observer(self)

    def __get_or_create_chat(self, chat_id: int) -> ITelegramChat:
        chat_instance: t.Optional[
            ITelegramChat
        ] = self.__telegram_chat_manager.get_chat(telegram_chat_id=chat_id)

        if chat_instance is not None:
            return chat_instance

        return self.__telegram_chat_manager.create_chat(chat_id)

    def __show_balance_command(self, event: BotCommandEvent) -> None:
        chat_instance: ITelegramChat = self.__get_or_create_chat(event.chat_id)

        pet: t.Optional[IPet] = self.__pet_engine_component.get_pet(
            chat_instance.get_id()
        )

        if not pet:
            tbot.send_message(
                chat_instance.chat_id,
                txt(chat_instance.language_code, "create_pet_first"),
            )
            return

        balance: t.Optional[IBalance] = self.__balance_engine_component.get_balance(
            pet.get_id()
        )

        if not balance:
            return

        tbot.send_message(
            chat_instance.chat_id,
            txt(chat_instance.language_code, "templates.balance").format(
                balance=balance.value
            ),
        )

    def __collect_bonus_command(self, event: BotCommandEvent) -> None:
        if not self.__periodic_money_bonus_engine_component:
            return

        chat_instance: ITelegramChat = self.__get_or_create_chat(event.chat_id)

        pet: t.Optional[IPet] = self.__pet_engine_component.get_pet(
            chat_instance.get_id()
        )

        if not pet:
            tbot.send_message(
                chat_instance.chat_id,
                txt(chat_instance.language_code, "create_pet_first"),
            )
            return

        balance: t.Optional[IBalance] = self.__balance_engine_component.get_balance(
            pet.get_id()
        )

        if not balance:
            return

        if not self.__periodic_money_bonus_engine_component.can_collect(pet.get_id()):
            tbot.send_message(
                chat_instance.chat_id,
                txt(
                    chat_instance.language_code,
                    "you_cant_collect_bonus_money_wait_more",
                ),
            )
            return

        delta: Decimal = self.__periodic_money_bonus_engine_component.collect(
            pet.get_id()
        )

        balance.value += delta

        tbot.send_message(
            chat_instance.chat_id, txt(chat_instance.language_code, "bonus_collected")
        )

    def notify(self, event: IEvent) -> None:
        if not isinstance(event, BotCommandEvent):
            return

        if event.command == "show_balance":
            self.__show_balance_command(event)
        elif event.command == "collect_bonus":
            self.__collect_bonus_command(event)
