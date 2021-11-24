from main import bot


@bot.message_handler(commands=['help'])
def command_help(message):
    bot.reply_to(message, "Введи комманду /start, чтобы начать. "
                          "В меню ты можешь посмотреть актуальные действия")