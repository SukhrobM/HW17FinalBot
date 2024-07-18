from telebot import types


def button_start():
    space = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but = types.KeyboardButton('Начнем!')
    space.add(but)
    return space


def button_phone():
    space = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but = types.KeyboardButton('Номер телефона📲', request_contact=True)
    space.add(but)
    return space


def button_loc():
    space = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but = types.KeyboardButton('Локация🌍🌍🌍', request_location=True)
    space.add(but)
    return space


def button_choice():
    space = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('Конвертор валют')
    but2 = types.KeyboardButton('Погода')
    space.add(but1, but2)
    return space


def currency_choice():
    cur_but_area = types.ReplyKeyboardMarkup(resize_keyboard=True)
    eutouz = types.KeyboardButton('EUR/UZS')
    uztoeu = types.KeyboardButton('UZS/EUR')
    cur_but_area.row(eutouz, uztoeu)
    ustouz = types.KeyboardButton('USD/UZS')
    uztous = types.KeyboardButton('UZS/USD')
    cur_but_area.row(ustouz, uztous)
    rutouz = types.KeyboardButton('RUB/UZS')
    uztoru = types.KeyboardButton('UZS/RUB')
    cur_but_area.row(rutouz, uztoru)
    gbtouz = types.KeyboardButton('GBP/UZS')
    uztogb = types.KeyboardButton('UZS/GBP')
    cur_but_area.row(gbtouz, uztogb)
    ret = types.KeyboardButton('Назад')
    cur_but_area.row(ret)
    return cur_but_area


def button_great():
    space = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but = types.KeyboardButton('Отлично')
    space.add(but)
    return space


def loop():
    markup = types.InlineKeyboardMarkup()
    but1 = types.InlineKeyboardButton(text='Повторить операцию',
                                      callback_data='repeat')
    markup.row(but1)
    but2 = types.InlineKeyboardButton(text='Вернуться на начало',
                                      callback_data='return')
    markup.row(but2)
    return markup


def weather_loop():
    markup = types.InlineKeyboardMarkup()
    but1 = types.InlineKeyboardButton(text='Повторить операцию',
                                      callback_data='weather_repeat')
    markup.row(but1)
    but2 = types.InlineKeyboardButton(text='Вернуться на начало',
                                      callback_data='weather_return')
    markup.row(but2)
    return markup
