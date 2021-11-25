import os

import flask
import telebot
from flask import Flask, request

from data.config import BOT_TOKEN
from utils.db_api.sqlite import Database
from utils.start_notify import on_startup_notify

bot = telebot.TeleBot(BOT_TOKEN)
db = Database(path_to_db="data/main.db")
server = Flask(__name__)


@server.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(flask.request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route('/', methods=["GET"])
def index():
    bot.remove_webhook()
    bot.set_webhook(url="https://agile-ridge-52994.herokuapp.com/{}".format(BOT_TOKEN))
    return "Hello from Heroku!", 200


if __name__ == '__main__':
    # это чтобы комманды отлавливались и выполнялись
    from handlers import *

    # база данных
    db.create_table_users()

    # уведомление админам
    on_startup_notify(bot)

    # bot.infinity_polling(skip_pending=True)
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    # вернуть web: gunicorn main:server в Procfile если webhook