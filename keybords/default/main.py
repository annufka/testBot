from telebot import types

markup_sex = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
markup_sex.add("Чоловік", "Жінка", "Назад")

markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
markup_main.add("Інфа про мене", "Настройки")

markup_settings = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
markup_settings.add("Змінити ім'я", "Змінити вік", "Змінити стать", "Назад")

markup_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_back.add("Назад")