import os

import telebot
from flask import Flask, request

from data.config import BOT_TOKEN, PORT
from utils.db_api.sqlite import Database
from utils.start_notify import on_startup_notify

bot = telebot.TeleBot(BOT_TOKEN)
db = Database(path_to_db="data/main.db")
# server = Flask(__name__)


# @server.route('/' + BOT_TOKEN, methods=['POST', 'GET'])
# def getMessage():
#     json_string = request.get_data().decode('utf-8')
#     update = telebot.types.Update.de_json(json_string)
#     bot.process_new_updates([update])
#     return "!", 200
#
#
# @server.route("/")
# def webhook():
#     bot.delete_webhook()
#     bot.set_webhook(url='https://agile-ridge-52994.herokuapp.com/' + BOT_TOKEN)
#     return "!", 200


if __name__ == '__main__':
    # это чтобы комманды отлавливались и выполнялись
    from handlers import *

    # база данных
    db.create_table_users()

    # уведомление админам
    # on_startup_notify(bot)

    bot.infinity_polling(skip_pending=True)
    # server.run(debug=True, host="0.0.0.0", port=int(os.environ.get('PORT', '5000')))
    # вернуть web: gunicorn main:server в Procfile если webhook