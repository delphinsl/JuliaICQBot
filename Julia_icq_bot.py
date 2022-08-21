from asyncio import events
from distutils.cmd import Command
from email.message import Message
from imaplib import Commands
#import logging
from pprint import pprint
from tracemalloc import start
from warnings import filters
from bot.bot import Bot
from bot.handler import BotButtonCommandHandler, StartCommandHandler, HelpCommandHandler, CommandHandler, UnknownCommandHandler
from bot.handler import MessageHandler
from bot.filter import Filter
from random import randrange, choice, random, shuffle
import os
import wikipedia
import random
import re
from datetime import date
import requests
import urllib.request
#import locale
from geopy.geocoders import Nominatim
import phonenumbers
import json
#from phonenumbers import geocoder
#from phonenumbers import timezone
#from phonenumbers import carrier


#logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
#        datefmt='%Y.%m.%d %I:%M:%S %p', level=logging.DEBUG)

TOKEN = "001.4280626070.2978902717:1005062871" #your token here
API_URL = "https://api.icq.net/bot/v1" #https://icq.im/Juliasun_bot

ibot = Bot(token=TOKEN, api_url_base=API_URL)

"""
#для распознавания речи
#import requests
import speech_recognition as sr
import subprocess
import datetime
import ffmpeg
import soundfile as sf
"""

wikipedia.set_lang("ru")
#locale.setlocale(category=locale.LC_ALL, 'ru_RU.UTF-8')
#local = locale.getlocale()
#token='5440755797:AAFrtl3HrvgNy-apBgltxngfMkF-ZX9y88g'
#bot=telebot.TeleBot(token)
#bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
token_yandex_w = 'cdf7b4b2-5476-4910-98c0-05726aefeed3'
token_yandex_geo = '2fb96aa2-7f13-4162-95dd-e086a1be43ea'

months = {
    'January' : 'января',
    'February' : 'февраля',
    'March' : 'марта',
    'April' : 'апреля',
    'May' : 'мая',
    'June' : 'июня',
    'July' : 'июля',
    'August' : 'августа',
    'September' : 'сентября',
    'October' : 'октября',
    'November' : 'ноября',
    'December' : 'декабря'
    }

@ibot.command_handler(command=['start', 'start1'])
def start_message(bot, event):
    bot.send_text(chat_id=event.from_chat, text=f'Привет {event.data["from"]["firstName"]}! Меня зовут Юля. Я ищу информацию в Википедии.')
    buttons = [
        [{"text": "Русский язык", "callbackData": "ru", "style": "primary"}],
        [{"text": "Английский язык", "callbackData": "en", "style": "primary"}],
        ]
    bot.send_text(chat_id=event.from_chat, text = 'Выберите язык для поиска', inline_keyboard_markup=buttons)
    bot.dispatcher.add_handler(BotButtonCommandHandler(callback=query_handler))
 
@ibot.command_handler(command=['stop1'])
def stop_message(bot, event):
	bot.send_text(chat_id=event.from_chat, text = 'Пока! Возвращайтесь.')

@ibot.command_handler(command=['help1'])
def welcome_help(bot, event):
    bot.send_text(chat_id=event.from_chat, text = 'Я знаю какой сегодня день и могу найти какой праздник в этот день. Чем я могу Вам помочь?')

@ibot.command_handler(command=['ru'])
def welcome_help_ru(bot, event):
    wikipedia.set_lang("ru")
    bot.send_text(chat_id=event.from_chat, text = 'Установлен русский язык')

@ibot.command_handler(command=['en'])
def welcome_help_en(bot, event):
    wikipedia.set_lang("en")
    bot.send_text(chat_id=event.from_chat, text = 'Установлен английский язык')

@ibot.message_handler(filters=['text'])
def send_text(bot, event):
    if event.text.lower() in ['привет','здравствуйте', 'добрый день', 'hello', 'hi', 'здорово', 'салют']:
        list_hi = ['Привет', 'Здравствуйте']
        #bot.send_message(message.chat.id, random.choice(list_hi)+' Меня зовут Юля. Я ищу информацию в Википедии.')
        bot.send_text(chat_id=event.from_chat, text = f'{random.choice(list_hi)} {event.data["from"]["firstName"]}! Меня зовут Юля. Я ищу информацию в Википедии.')
        bot.send_text(chat_id=event.from_chat, text =' Что Вы ищите ?')
    elif event.text.lower() in ['пока','до свидания', 'до встречи','счастливо','прощай','пока пока']:
        list_bye = ['Пока! Возвращайтесь.', 'До свидания!', 'До скорой встречи!']
        bot.send_text(chat_id=event.from_chat, text = random.choice(list_bye))
        btn_url = [{"text": 'Поддержать проект', "url": 'https://netmonet.ru/s/user4150'}]
        bot.answer_callback_query(query_id=event.data['queryId'], text = '', url = '', separate_message='url pressed', inline_keyboard_markup=btn_url)
        bot.dispatcher.add_handler(BotButtonCommandHandler(callback=btn_url, filters=Filter.callback_data("btn_url")))
        #bot.dispatcher.add_handler(MessageHandler(callback=btn_url))

        bot.send_text(chat_id=event.from_chat, text = 'Спасибо, что воспользовались ботом!')
    elif event.text.lower() == 'спасибо':
        bot.send_text(chat_id=event.from_chat, text = 'Пожалуйста!')
        bot.send_text(chat_id=event.from_chat, text = 'Что-то еще?')
    elif event.text.lower() in ['кто твой создатель', 'кто тебя сделал', 'кто разработчик', 'кто тебя создал', 'создатель', 'разработчик']:
        bot.send_text(chat_id=event.from_chat, text = 'https://t.me/delphinsoftltd')
    elif event.text.lower() in ['какой сегодня день', 'какой день сегодня', 'какой сегодня праздник', 'какой праздник сегодня', 'какой сегодня день?', 'какой день сегодня?', 'какой сегодня праздник?', 'какой праздник сегодня?']:
        #day = event.text
        current_date = date.today()      
        current_date_today = current_date.strftime('%d %B %Y').split(' ')
        month = months[current_date_today[1]]
        current_date_today = f'{current_date_today[0]} {month} {current_date_today[2]}'
        if event.text.lower() in ['какой сегодня день', 'какой день сегодня', 'какой сегодня день?', 'какой день сегодня?']:
            bot.send_text(chat_id=event.from_chat, text = f'Сегодня {current_date_today}')
        elif event.text.lower() in ['какой сегодня праздник', 'какой праздник сегодня', 'какой сегодня праздник?', 'какой праздник сегодня?']:
            try:
                current_date = current_date.strftime(f'%d {month}')
                holiday = 'праздник ' + current_date                
                bot.send_text(chat_id=event.from_chat, text = wikipedia.summary(holiday))
            except Exception as e:
                bot.send_text(chat_id=event.from_chat, text = f'В энциклопедии нет информации об этом {holiday}')
    else:
        #keyboard = telebot.types.ReplyKeyboardMarkup(True)
        #keyboard.row('спасибо')
        titles = ''
        titles = event.text.lower()
        titles_2 = wikipedia.search(titles)
        try:
            bot.send_text(chat_id=event.from_chat, text = f'*Вот что мне удалось найти:*\n\n{wikipedia.summary(titles)}', parse_mode='MarkdownV2') #, parseMode ='MarkdownV2'
            bot.send_text(chat_id=event.from_chat, text = 'Чтобы узнать подробнее, нажмите на ссылку ниже')
            bot.send_text(chat_id=event.from_chat, text = f'{urllib.parse.unquote(wikipedia.page(titles).url)}') #reply_markup=keyboard
            #bot.send_message(message.chat.id, wikipedia.page(titles).url, reply_markup=keyboard)
            #markup = telebot.types.InlineKeyboardMarkup()
            #markup.add(telebot.types.InlineKeyboardButton(text=str(wikipedia.page(titles).url), url=wikipedia.page(titles).url)) 
            #bot.send_message(message.chat.id, wikipedia.page(titles).url, reply_markup=markup)
            bot.send_text(chat_id=event.from_chat, text = 'Если не то, что Вы искали, попробуйте выбрать из списка ниже и повторить запрос:')
            bot.send_text(chat_id=event.from_chat, text = ", ".join(titles_2))
            #bot.answer_callback_query(query_id=event.data['queryId'], text='', inline_keyboard_markup=btn_thanks)

        except Exception as e:
            bot.send_text(chat_id=event.from_chat, text = 'В энциклопедии нет информации об этом. Поищу в Яндексе')
            response = requests.get(url = 'https://yandex.ru/search/', params={'text': titles, 'lr': 213})
            bot.send_text(chat_id=event.from_chat, text = response.url)


#функция ответа на фото
#@bot.photo_handler(filters=['photo'])
def photo_handler(bot, event):
    bot.send_text(chat_id=event.from_chat, text = 'Красиво')

#функция ответа на стикер
#@ibot.message_handler(filters=['sticker'])
def sticker_handler(bot, event):
    bot.send_text(chat_id=event.from_chat, text = 'Твой стикер смешной')

#функция ответа на локацию
def what_weather(city):
    url = f'http://wttr.in/{city}'
    weather_parameters = {
        'format': 2,
        '0': '',
        'T':'',
        'M':'',
        'lang': 'ru'
    }
    try:
        response = requests.get(url, params=weather_parameters)
    except requests.ConnectionError:
        return 'Сетевая ошибка'
    if response.status_code == 200:
        return response.text
        print(response.text)
    else:
        return 'Ошибка на сервере погоды'

#@bot.location_handler#(filters=['location'])
def loc_handler(bot, event):  
    try:
        #current_position = (event.location.latitude, event.location.longitude)
        #current_position = (event.data.json())# location.latitude, event.location.longitude)
        longitude = event.data["text"].split('=')[2].split(',')[1]
        latitude = event.data["text"].split('=')[2].split(',')[0]
        coords = f'{latitude},{longitude}'
        geolocator = Nominatim(user_agent="juliasun_bot")
        location = geolocator.reverse(coords)
        #city = str(location).split(', ')
        address = location.raw["address"]
        citi = address.get('city', '')
        town = address.get('town', '')
        bot.send_text(chat_id=event.from_chat, text = f'*Вы находитесь:* {location}', parse_mode='MarkdownV2')
        if citi != '':
            #bot.send_text(chat_id=event.from_chat, text = f'*Погода сейчас:*\n{what_weather(citi)}', parse_mode='MarkdownV2')
            nom = what_weather(citi)
        else:
            #bot.send_text(chat_id=event.from_chat, text = f'*Погода сейчас:*\n{what_weather(town)}', parse_mode='MarkdownV2')
            nom = what_weather(town)
        
        url_ya = f'https://api.weather.yandex.ru/v2/forecast?&lat={latitude}&lon={longitude}&[lang=ru_RU]'
        #bot.send_message(message.chat.id, url_ya)
        resp = requests.get(url_ya, headers={'X-Yandex-API-Key': token_yandex_w}, verify=True)
        yandex_json = json.loads(resp.text)
        #bot.send_text(chat_id=event.from_chat, text = yandex_json['info']['url'])

        conditions = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
                    'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
                    'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
                    'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
                    'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
                    'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
                    'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
                    }
        wind_dir = {'nw': 'северо-западное', 'n': 'северное', 'ne': 'северо-восточное', 'e': 'восточное',
                    'se': 'юго-восточное', 's': 'южное', 'sw': 'юго-западное', 'w': 'западное', 'с': 'штиль'}
        temp = yandex_json['fact']['temp']
        fl = yandex_json['fact']['feels_like']
        icon = yandex_json['fact']['icon']
        cond = conditions[yandex_json['fact']['condition']]
        pres = yandex_json['fact']['pressure_mm']
        presp = yandex_json['fact']['pressure_pa']
        hum = yandex_json['fact']['humidity']
        ws = yandex_json['fact']['wind_speed']
        wg = yandex_json['fact']['wind_gust']
        wd = wind_dir[yandex_json['fact']['wind_dir']]
        dt = yandex_json['fact']['daytime']
        link = yandex_json['info']['url']
        icon_url = f'https://yastatic.net/weather/i/icons/funky/dark/{icon}.svg'
        bot.send_text(chat_id=event.from_chat, text = f'https://yastatic.net/weather/i/icons/funky/dark/{icon}.svg')
        bot.send_text(chat_id=event.from_chat, text = f'*Погода сейчас:*\n{nom}\nСостояние: {cond}\nТемпература: {temp} °C\n\
Ощущается как: {fl} °C\nВлажность: {hum} %\nАтмосферное давление: {pres} мм.рт.ст.\n\
Направление ветра: {wd}\nСкорость ветра: {ws} м/с\nПорывы ветра: {wg} м/с\n{link}', 
parse_mode='MarkdownV2')
        #bot.send_text(chat_id=event.from_chat, text = f'https://yastatic.net/weather/i/icons/funky/dark/{icon}.svg')
    except Exception as e:
        bot.send_text(chat_id=event.from_chat, text = 'Уточните локацию')
    

#функция ответа на контакт
#@bot.contact_handler(filters=['contact'])
def cont_handler(bot, event):
    number_phone = event.text
    if not number_phone.startswith('+'):
        number_phone = (number_phone).replace('8', '+7', 1)
    number_phone = phonenumbers.parse(number_phone, 'ru')
    country = phonenumbers.geocoder.description_for_number(number_phone, 'ru')
    provider = phonenumbers.carrier.name_for_number(number_phone, 'ru')
    #bot.send_message(message.chat.id, provider)
    try:
        if country =='' and provider !='':
            bot.send_text(chat_id=event.from_chat, text = f'Оператор: {provider}')
        elif country !='' and provider =='':
            bot.send_text(chat_id=event.from_chat, text = f'Регион: {country}')
        elif country !='' and provider !='':
            bot.send_text(chat_id=event.from_chat, text = f'Регион: {country}, оператор: {provider}')
        else:
            bot.send_text(chat_id=event.from_chat, text = f'Неизвестный формат номера {number_phone}') 
    except Exception as e:
        bot.send_text(chat_id=event.from_chat, text = 'Это точно контакт')
    

#функция ответа на другие типы документов
#@bot.message_handler(filters=['audio', 'video', 'media'])
def any_handler(bot, event):
    bot.send_text(chat_id=event.from_chat, text='Я не знаю, что с этим делать. Что Вы ищите?')

#функция выбора языка для поиска в википедии
#@bot.command_handler #.query_handler#(func=lambda call: True)
def query_handler(bot, event):
    if event.data['callbackData'] == "ru":
        wikipedia.set_lang("ru")
        bot.answer_callback_query(query_id=event.data['queryId'], text='', show_alert=False)
        bot.send_text(chat_id=event.from_chat, text='Установлен русский язык')
    elif event.data['callbackData'] == "en":
        wikipedia.set_lang("en")
        bot.answer_callback_query(query_id=event.data['queryId'], text='', show_alert=False)
        bot.send_text(chat_id=event.from_chat, text='Установлен английский язык')
    bot.send_text(chat_id=event.from_chat, text = 'Что Вы ищите ?')

#def btn_thanks(bot, event):
#    sender(bot, chat_id=event.data['message']['chat']['chatId'],
#           query_id=event.data['queryId'],
#           text='Спасибо',  separate_message='Спасибо',
#           )

def main():
    bot = Bot(token=TOKEN, api_url_base=API_URL)

    bot.dispatcher.add_handler(StartCommandHandler(callback=start_message))
    bot.dispatcher.add_handler(CommandHandler(command='stop1', filters=Filter.command, callback=stop_message))
    bot.dispatcher.add_handler(CommandHandler(command='help1', filters=Filter.command, callback=welcome_help))
    bot.dispatcher.add_handler(CommandHandler(command='ru', filters=Filter.command, callback=welcome_help_ru))
    bot.dispatcher.add_handler(CommandHandler(command='en', filters=Filter.command, callback=welcome_help_en))
    bot.dispatcher.add_handler(MessageHandler(filters=Filter.text, callback=send_text))
    bot.dispatcher.add_handler(MessageHandler(filters=Filter.sticker, callback=sticker_handler))
    bot.dispatcher.add_handler(MessageHandler(filters=Filter.image, callback=photo_handler))
    bot.dispatcher.add_handler(MessageHandler(filters=Filter.video & Filter.audio, callback=any_handler))
    bot.dispatcher.add_handler(MessageHandler(filters=Filter.url, callback=loc_handler))
    #if bot.events_get== 
    #bot.dispatcher.add_handler(UnknownCommandHandler(filters=Filter.text, callback=cont_handler))

    
    #bot.dispatcher.add_handler(MessageHandler(callback=photo_handler, filters=Filter.image))
    #bot.dispatcher.add_handler(sticker_handler)#, filters=Filter.sticker)
    #bot.dispatcher.add_handler(BotButtonCommandHandler(callback=btn_thanks, filters=Filter.callback_data("спасибо")))
    
    #bot.dispatcher.add_handler(CommandHandler(callback=welcome_help))
    #bot.dispatcher.add_handler(BotButtonCommandHandler(
    #    callback=start_message, filters=Filter.callback_data("start_message")))    
    #bot.dispatcher.add_handler(BotButtonCommandHandler(
    #    callback=stop_message, filters=Filter.callback_data("stop_message")))
    
    #bot.dispatcher.add_handler(BotButtonCommandHandler(
    #    callback=wrong, filters=Filter.callback_data("wrong")))
    #bot.dispatcher.add_handler(BotButtonCommandHandler(
    #    callback=right, filters=Filter.callback_data("right")))
    bot.start_polling()

    bot.idle()    
    
# ---------------- local testing ----------------
if __name__ == '__main__':
    main()
