from keybords.default.main import markup_sex, markup_main, markup_back
from main import bot, db

from telebot import types

user_dict = {}


class UserData:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None


@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    msg = bot.send_message(message.chat.id, "Привіт! Введи своє ім'я")
    bot.register_next_step_handler(msg, enter_name)


def enter_name(message: types.Message):
    name = message.text
    if len(name) >= 2 and len(name) <= 20:
        user = UserData(name)
        user_dict[message.chat.id] = user
        msg = bot.send_message(message.chat.id, "Введіть свій вік", reply_markup=markup_back)
        bot.register_next_step_handler(msg, enter_age)
    else:
        msg = bot.reply_to(message,
                           "І що це ти мені ввів? Ім'я повинно містити не менше двох символів і не більше двадцяти. Спробуй ще раз",
                           reply_markup=markup_back)
        bot.register_next_step_handler(msg, enter_name)
        return


def enter_age(message: types.Message):
    # верю, что вот это назад можно получить красивее, но я делаю так впервые и это единственное что пока пришло в голову)
    if message.text != "Назад":
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, "Вік не може містити букви, спробуй ще раз", reply_markup=markup_back)
            bot.register_next_step_handler(msg, enter_age)
            return
        elif age.isdigit():
            if (int(age) >= 2 and int(age) <= 102):
                user = user_dict[message.chat.id]
                user.age = int(age)
                msg = bot.send_message(message.chat.id, "Обери на клавіатурі свою стать", reply_markup=markup_sex)
                bot.register_next_step_handler(msg, enter_sex)
            else:
                msg = bot.reply_to(message, 'Вік повинен бути більше 2 і менше 102', reply_markup=markup_back)
                bot.register_next_step_handler(msg, enter_age)
                return
    else:
        msg = bot.send_message(message.chat.id, "Привіт! Введи своє ім'я")
        bot.register_next_step_handler(msg, enter_name)


def enter_sex(message: types.Message):
    if message.text != "Назад":
        sex = message.text
        user = user_dict[message.chat.id]
        if (sex == "Чоловік") or (sex == "Жінка"):
            user.sex = sex
            try:
                db.add_user(telegram_id=message.chat.id, name=user.name, age=user.age, sex=user.sex)
                bot.send_message(message.chat.id, "Дякую за відповіді, я все записав", reply_markup=markup_main)
            except:
                bot.send_message(message.chat.id,
                                 "Щось пішло не так, коли я записував твої данні, нажми /start та запиши ще раз свої дані.",
                                 reply_markup=None)
        else:
            msg = bot.reply_to(message, "Ну що ти за людина, обери ж свою стать!", reply_markup=markup_sex)
            bot.register_next_step_handler(msg, enter_sex)
            return
    else:
        msg = bot.send_message(message.chat.id, "Введіть свій вік", reply_markup=markup_back)
        bot.register_next_step_handler(msg, enter_age)

@bot.edited_message_handler(content_types=['text'])
def check_new_info(message: types.Message):
    bot.reply_to(message, "Что ты тут уже редактируешь, руки прочь!")