# подключаем библиотеку для работы с запросами
import requests
import telebot
from telebot import types

bot = telebot.TeleBot('6428000289:AAFhJCdvXcaQpVPiPF2HPkakGj2MZAivcPI')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, я могу предсказать погоду "
                                               "или рассказать про python, введи /help")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет, название города или /python")
    elif message.text == "/python":
        mesg = bot.send_message(message.chat.id, 'Начнем?')
        bot.register_next_step_handler(mesg, get_python)
    else:
        # получаем город из сообщения пользователя
        city = message.text
        # формируем запрос
        url = ('https://api.openweathermap.org/data/2.5/weather?q='
               + city + '&units=metric&lang=ru&appid=f09bf0b1069b265f86a2b8a52b7dc6f9')
        # отправляем запрос на сервер и сразу получаем результат
        weather_data = requests.get(url).json()
        # получаем данные о температуре и о том, как она ощущается
        temperature = round(weather_data['main']['temp'])
        temperature_feels = round(weather_data['main']['feels_like'])
        # формируем ответы
        w_now = 'Сейчас в городе ' + city + ' ' + str(temperature) + ' °C'
        w_feels = 'Ощущается как ' + str(temperature_feels) + ' °C'
        # отправляем значения пользователю
        bot.send_message(message.from_user.id, w_now)
        bot.send_message(message.from_user.id, w_feels)
def get_python(message):
    keyboard = types.InlineKeyboardMarkup() #наша клавиатура
    key_history = types.InlineKeyboardButton(text='Этапы развития языка Python', callback_data='history')
    keyboard.add(key_history) #добавляем кнопку в клавиатуру
    key_features= types.InlineKeyboardButton(text='Особенности языка Python', callback_data='features')
    keyboard.add(key_features)
    key_type = types.InlineKeyboardButton(text='Переменные. Типы данных. Операторы', callback_data='type')
    keyboard.add(key_type)
    key_structure = types.InlineKeyboardButton(text='Структуры данных', callback_data='structure')
    keyboard.add(key_structure)
    question = 'Что тебя интересует по Python?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "history": #call.data это callback_data, которую мы указали при объявлении кнопки
        #код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id,
        '1991 год. Программист из Нидерландов Гвидо ван Россум разработал язык программирования Python.\n'
        '1995 год. В этом году появилась компания «Python Software Foundation»\n'
        '2008 год. К этому моменту появилась третья версия языка Python,'
        'в которой были устранены многие недостатки архитектуры с максимально возможной совместимостью со старыми версиями.\n'
        '2020 год. С этого момента официальное Python-сообщество поддерживает только третью версию языка')
    elif call.data == "features":
        bot.send_message(call.message.chat.id, '1. Интроспекция.\n'
                                               '2. Мультиплатформеность.\n'
                                               '3. Библиотеки.\n'
                                               '4. Читаемость языка.\n'
                                               '5. Низкое быстродействие.\n')
    elif call.data == "type":
        bot.send_message(call.message.chat.id, '1. Числовые типы данных: целые числа (int), числа с плавающей запятой (float).\n'
                                               '2. Строковые типы данных: строки (str).\n'
                                               '3. Логический тип данных: булев тип (bool) со значениями True и False.\n')
    elif call.data == "structure":
        bot.send_message(call.message.chat.id, 'Изменяемые типы данных могут быть изменены после создания. Когда вы изменяете изменяемый объект,'
                                               'вы изменяете его исходное значение. Примером изменяемых типов'
                                               'данных являются преимущественно коллекции, о которых мы поговорим далее (list, set, dict).')

if __name__ == '__main__':
    while True:
        # в бесконечном цикле постоянно опрашиваем бота — есть ли новые сообщения
        try:
            bot.polling(none_stop=True, interval=0)
        # если возникла ошибка — сообщаем про исключение и продолжаем работу
        except Exception as e:
            print('Сработало исключение!')
