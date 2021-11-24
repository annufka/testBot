import telebot

from data.config import BOT_TOKEN
from utils.db_api.sqlite import Database

bot = telebot.TeleBot(BOT_TOKEN)
db = Database(path_to_db="data/main.db")

if __name__ == '__main__':
    # это чтобы комманды отлавливались и выполнялись
    from handlers import *

    # база данных
    db.create_table_users()

    bot.infinity_polling()
