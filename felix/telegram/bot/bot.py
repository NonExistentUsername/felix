import os
from telebot import TeleBot

TG_BOT_TOKEN = str(os.getenv("TG_BOT_TOKEN"))

tbot: TeleBot = TeleBot(TG_BOT_TOKEN)