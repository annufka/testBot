from keybords.default.main import markup_settings, markup_sex, markup_main, markup_back
from main import bot, db
from telebot import types

edit_user_dict = {}


class EditingParam:
    def __init__(self):
        self.param = None
        self.value = None


@bot.message_handler(content_types=['text'])
def return_about_user(message: types.Message):
    if message.text == "Інфа про мене":
        try:
            info = db.select_user(message.chat.id)
            bot.send_message(message.chat.id, f"Ім'я - {info[1]},\nвік - {info[2]},\nстать - {info[3]}")
        except:
            bot.send_message(message.chat.id, "Щось пішло не так, спробуй ще")
    elif message.text == "Настройки":
        msg = bot.send_message(message.chat.id, "Обери, що ти хочеш змінити", reply_markup=markup_settings)
        bot.register_next_step_handler(msg, enter_param)


def enter_param(message: types.Message):
    user = EditingParam()
    edit_user_dict[message.chat.id] = user
    if message.text == "Змінити ім'я":
        user.param = "name"
        msg = bot.send_message(message.chat.id, "Введіть нове значення або нажміть назад", reply_markup=markup_back)
        bot.register_next_step_handler(msg, edit_param)
    elif message.text == "Змінити вік":
        user.param = "age"
        msg = bot.send_message(message.chat.id, "Введіть нове значення або нажміть назад", reply_markup=markup_back)
        bot.register_next_step_handler(msg, edit_param)
    elif message.text == "Змінити стать":
        user.param = "sex"
        msg = bot.send_message(message.chat.id, "Оберіть стать або нажміть назад", reply_markup=markup_sex)
        bot.register_next_step_handler(msg, edit_param)
    # Назад сюда пойдет
    else:
        bot.send_message(message.chat.id, "Обери функцію", reply_markup=markup_main)
        return


def edit_param(message: types.Message):
    user = edit_user_dict[message.chat.id]
    if message.text != "Назад":
        value = message.text
        # вот тут я задумалась о смысле всех этих условий, но мне же надо как-то отвалидироваться, но и повторять в каждом
        # условии, что присвоить значение бесполезно, поэтому пока просто pass. Можно было написать что-то типо вы меняете,
        # например, пол с такого-то на такой-то
        if user.param == "name" and len(value) >= 2 and len(value) <= 20:
            pass
        elif user.param == "age" and value.isdigit():
            if int(value) >= 2 and int(value) <= 102:
                pass
        elif user.param == "sex" and value in ("Чоловік", "Жінка"):
            pass
        else:
            if user.param == "sex":
                msg = bot.send_message(message.chat.id, "Щось ти не те робиш!  Оберить стать або нажміть назад",
                                       reply_markup=markup_sex)
                bot.register_next_step_handler(msg, edit_param)
                return
            else:
                msg = bot.send_message(message.chat.id, "Щось ти не те робиш! Введи значення або нажміть назад")
                bot.register_next_step_handler(msg, edit_param)
                return
            user.value = value
        db.edit_param(message.chat.id, user.param, value)
        # вот кстати интересно, в aiogram state можно завершить, а тут что делать с нечтом, что создал пользователь?
        bot.send_message(message.chat.id, "Записано", reply_markup=markup_main)
    else:
        # мне показалось логичнее здесь возвращаться на выбор параметра изменения, чем на былор того же что и предлагалось
        msg = bot.send_message(message.chat.id, "Обери, що ти хочеш змінити", reply_markup=markup_settings)
        bot.register_next_step_handler(msg, enter_param)
        return
