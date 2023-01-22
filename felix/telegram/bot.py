import os
import logging
from telebot import TeleBot, logger

TG_BOT_TOKEN = str(os.getenv("TG_BOT_TOKEN"))

tbot: TeleBot = TeleBot(TG_BOT_TOKEN)

DEBUG = os.getenv("DEBUG") == "True"

if DEBUG:
    logger.setLevel(logging.DEBUG)
