import logging
import os
import time
from uuid import uuid4

import flask
import telebot

from .bot import tbot

DEBUG = os.getenv("DEBUG") == "True"
API_TOKEN = str(os.getenv("TG_BOT_TOKEN"))

WEBHOOK_HOST = str(os.getenv("HOST"))
WEBHOOK_PORT = 8443
WEBHOOK_LISTEN = "0.0.0.0"

WEBHOOK_SSL_CERT = "/app/cert/ssl.crt"
WEBHOOK_SSL_PRIV = "/app/cert/ssl.key"

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)
SECRET = str(uuid4())


app = flask.Flask(__name__)


@app.route("/")
def home():
    return ""


@app.route(WEBHOOK_URL_PATH, methods=["POST"])
def webhook():
    if not flask.request.headers.get("content-type") == "application/json":
        flask.abort(403)

    if not flask.request.headers.get("X-Telegram-Bot-Api-Secret-Token") == SECRET:
        flask.abort(403)

    json_string = flask.request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    if update is None:
        return ""
    tbot.process_new_updates([update])
    return ""


def run_app():
    tbot.remove_webhook()

    time.sleep(1)

    tbot.set_webhook(
        url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
        certificate=open(WEBHOOK_SSL_CERT, "r"),
        secret_token=SECRET,
    )

    app.run(
        host=WEBHOOK_LISTEN,
        port=8080,
        debug=DEBUG,
    )
