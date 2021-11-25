from data.config import ADMINS

def on_startup_notify(bot):
    for admin in ADMINS:
        try:
            bot.send_message(admin, "Бот Запущен")

        except Exception as err:
            print("Щось не то")
