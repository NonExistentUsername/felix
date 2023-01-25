import logging
import time

import flask
import telebot

from .bot import tbot

API_TOKEN = "<api_token>"

WEBHOOK_HOST = "<ip/host where the bot is running>"
WEBHOOK_PORT = 8443
WEBHOOK_LISTEN = "0.0.0.0"

WEBHOOK_SSL_CERT = "./webhook_cert.pem"
WEBHOOK_SSL_PRIV = "./webhook_pkey.pem"

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)


app = flask.Flask(__name__)


@app.route("/", methods=["GET", "HEAD"])
def index():
    return ""


@app.route(WEBHOOK_URL_PATH, methods=["POST"])
def webhook():
    if flask.request.headers.get("content-type") == "application/json":
        json_string = flask.request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        if update is None:
            return ""
        tbot.process_new_updates([update])
        return ""
    else:
        flask.abort(403)


tbot.remove_webhook()

time.sleep(0.1)

tbot.set_webhook(
    url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, "r")
)

app.run(
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT,
    ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
    debug=True,
)
