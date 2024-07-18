import telebot
import requests
import json
import buttons as bt
import database as db


# https://t.me/INeedYourNumber2Bot
bot = telebot.TeleBot('7259903359:AAGhczImvNVoAWRXSL5u8PV4ysMxTq0o7CY') # Токен
API = '719e149a83e24d1709014f2e2fb68e80' # API для информации о погоде
## Отсюда берем курсы валют ##
response = requests.get('https://cbu.uz/ru/arkhiv-kursov-valyut/json/')
x = response.json()
c_list = ['EUR/UZS', 'UZS/EUR', 'USD/UZS', 'UZS/USD', 'RUB/UZS', 'UZS/RUB', 'GBP/UZS', 'UZS/GBP']


## Стартовое сообщение ##
@bot.message_handler(commands=['start'])
def welcome(msg):
    user_id = msg.from_user.id
    bot.send_message(user_id, 'Давайте начнем работу',
                     reply_markup=bt.button_start())


## Проверка регистрации ##
@bot.message_handler(content_types=['text'])
def check_user(msg):
    user_id = msg.from_user.id
    check = db.check_user(user_id)
    if check:
        check_name = db.check_name(user_id)[1]
        bot.send_message(user_id, f'Привет {check_name}! Что ты хочешь узнать?',
                         reply_markup=bt.button_choice())
        bot.register_next_step_handler(msg, make_choice)
    else:
        bot.send_message(user_id, 'Давайте добавим вас в базу\n Напишите свое имя',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_name)


# Выбор операций после прохождения проверки
def make_choice(msg):
    user_id = msg.from_user.id
    if msg.text == 'Конвертор валют':
        bot.send_message(user_id, 'Выберите метод конвертацтии',
                         reply_markup=bt.currency_choice())
        bot.register_next_step_handler(msg, convert_input)
    elif msg.text == 'Погода':
        bot.send_message(user_id, 'Напиши название города',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, weather)
    elif msg.text == "/start":
        bot.send_message(user_id, 'Давайте начнем работу',
                         reply_markup=bt.button_start())
        bot.register_next_step_handler(msg, check_user)
    else:
        bot.send_message(user_id, 'Выберите вариант по кнопкам')
        bot.register_next_step_handler(msg, make_choice)


## Конвертор валют ##
# Выбор валюты
def convert_input(msg):
    user_id = msg.from_user.id
    val = msg.text
    if val in c_list:
        bot.send_message(user_id, 'Введите сумму, которую хотите конвертировать',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, convert_result, val)
    elif val == 'Назад':
        check_name = db.check_name(user_id)[1]
        bot.send_message(user_id, f'Привет {check_name}! Что ты хочешь узнать?',
                         reply_markup=bt.button_choice())
        bot.register_next_step_handler(msg, make_choice)
    else:
        bot.send_message(user_id, 'Неверные данные. Выбрите одну из кнопок',
                         reply_markup=bt.currency_choice())
        bot.register_next_step_handler(msg, convert_input)


# Выдача результатов
def convert_result(msg, val):
    user_id = msg.from_user.id
    try:
        count = int(msg.text)
        if val == 'EUR/UZS':
            euro = round(count * float(x[1]['Rate']), 2)
            bot.send_message(user_id, f'{str(euro)} сум', reply_markup=bt.loop())
        elif val == 'USD/UZS':
            us_dollar = round(count * float(x[0]['Rate']), 2)
            bot.send_message(user_id, f'{str(us_dollar)} сум', reply_markup=bt.loop())
        elif val == 'RUB/UZS':
            ruble = round(count * float(x[2]['Rate']), 2)
            bot.send_message(user_id, f'{str(ruble)} сум', reply_markup=bt.loop())
        elif val == 'GBP/UZS':
            pound = round(count * float(x[3]['Rate']), 2)
            bot.send_message(user_id, f'{str(pound)} сум', reply_markup=bt.loop())
        elif val == 'UZS/EUR':
            pound = round(count * 1 / float(x[1]['Rate']), 2)
            bot.send_message(user_id, f'{str(pound)} EUR', reply_markup=bt.loop())
        elif val == 'UZS/USD':
            pound = round(count * 1 / float(x[0]['Rate']), 2)
            bot.send_message(user_id, f'{str(pound)} USD', reply_markup=bt.loop())
        elif val == 'UZS/RUB':
            pound = round(count * 1 / float(x[2]['Rate']), 2)
            bot.send_message(user_id, f'{str(pound)} RUB', reply_markup=bt.loop())
        elif val == 'UZS/GBP':
            pound = round(count * 1 / float(x[1]['Rate']), 2)
            bot.send_message(user_id, f'{str(pound)} GBP', reply_markup=bt.loop())
    except ValueError:
        bot.send_message(user_id, 'Введите сумму, которую хотите конвертировать')
        bot.register_next_step_handler(msg, convert_result, val)
    return


@bot.callback_query_handler(lambda call: call.data in ['repeat', 'return'])
def loop_choice(call):
    if call.data == 'repeat':
        bot.send_message(call.message.chat.id,
                         'Выберите метод конвертацтии',
                         reply_markup=bt.currency_choice())
        bot.register_next_step_handler(call.message, convert_input)
    elif call.data == 'return':
        bot.send_message(call.message.chat.id,
                         'Давайте начнем работу',
                         reply_markup=bt.button_start())
        bot.register_next_step_handler(call.message, check_user)


## Погода ##
def weather(msg):
    city = msg.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        pres = data["main"]["pressure"]
        hum = data["main"]["humidity"]
        bot.send_message(msg.chat.id, f'Сейчас погода {temp}°\n '
                                      f'Давление {pres} гПа\n Влажность {hum}%')

        def image(main):
            if main == "Clear":
                return "sunny.png"
            elif main == "Clouds":
                return "clouds.png"
            elif main == "Rain":
                return "rain.png"
            elif main == "Mist":
                return "mist.png"
            elif main == "Drizzle":
                return "drizzle.png"
            elif main == "Snow":
                return "snow.png"

        file = open('./' + image(main=data["weather"][0]["main"]), 'rb')
        bot.send_photo(msg.chat.id, file, reply_markup=bt.weather_loop())
    else:
        bot.send_message(msg.chat.id, 'Введите правильное название города')
        bot.register_next_step_handler(msg, weather)


@bot.callback_query_handler(lambda call: call.data in ['weather_repeat', 'weather_return'])
def loop_weather(call):
    if call.data == 'weather_repeat':
        bot.send_message(call.message.chat.id,
                         'Напиши название города')
        bot.register_next_step_handler(call.message, weather)
    elif call.data == 'weather_return':
        bot.send_message(call.message.chat.id,
                         'Давайте начнем работу', reply_markup=bt.button_start())
        bot.register_next_step_handler(call.message, check_user)


## Регистрация ##
# Введение номера
def get_name(msg):
    user_id = msg.from_user.id
    user_name = msg.text
    bot.send_message(user_id, 'Имя зарегестрировано! Теперь введите свой номер',
                     reply_markup=bt.button_phone())
    bot.register_next_step_handler(msg, get_number, user_name)


# Введение локации
def get_number(msg, user_name):
    user_id = msg.from_user.id
    if msg.contact:
        user_number = msg.contact.phone_number
        bot.send_message(user_id, 'Номер зарегестрирован! Теперь отправьте свою локацию',
                         reply_markup=bt.button_loc())
        bot.register_next_step_handler(msg, get_location, user_name, user_number)
    else:
        bot.send_message(user_id, 'Отправьте номер через кнопку!')
        bot.register_next_step_handler(msg, get_number, user_name)


# Регистрация в базе данных
def get_location(msg, user_name, user_number):
    user_id = msg.from_user.id
    if msg.location:
        user_location_lat = msg.location.latitude
        user_location_lng = msg.location.longitude
        db.registration(user_id, user_name, user_number,
                        user_location_lat, user_location_lng)
        bot.send_message(user_id, 'Локация принята! Вы зарегестрированы в базе данных',
                         reply_markup=bt.button_great())
        bot.register_next_step_handler(msg, check_user)
    else:
        bot.send_message(user_id, 'Отправьте локацию через кнопку!')
        bot.register_next_step_handler(msg, get_location, user_name, user_number)


bot.polling(non_stop=True)
