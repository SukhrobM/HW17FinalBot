import telebot
from telebot import types
from currency_converter import CurrencyConverter


cur = CurrencyConverter()
bot = telebot.TeleBot('7259903359:AAGhczImvNVoAWRXSL5u8PV4ysMxTq0o7CY')
amount = 0


@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, 'Привет! Введите сумму')
    bot.register_next_step_handler(msg, somesum)


def somesum(msg):
    global amount
    try:
        amount = int(msg.text.strip())
    except ValueError:
        bot.send_message(msg.chat.id, 'Попробуйте еще раз. ВВедите корректную сумму')
        bot.register_next_step_handler(msg, somesum)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        but1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        but2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        but3 = types.InlineKeyboardButton('USD/GBR', callback_data='usd/gbp')
        but4 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(but1, but2, but3, but4)
        bot.send_message(msg.chat.id, 'Выберите пару валют', reply_markup=markup)
    else:
        bot.send_message(msg.chat.id, 'Число должно быть больше 0')
        bot.register_next_step_handler(msg, somesum)


@bot.callback_query_handler(lambda call: True)
def callback(call):
    if call.data != 'else':
        value = call.data.upper().split('/')
        res = cur.convert(amount, value[0], value[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму')
        bot.register_next_step_handler(call.message, somesum)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару значений через (/) слеш')
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(msg):
    try:
        value = msg.text.upper().split('/')
        res = cur.convert(amount, value[0], value[1])
        bot.send_message(msg.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму')
        bot.register_next_step_handler(msg, somesum)
    except Exception:
        bot.send_message(msg.chat.id, f'Неверные данные, введите значение в формате (ААА/ААА) для определения валют')
        bot.register_next_step_handler(msg, my_currency)


bot.polling(non_stop=True)
