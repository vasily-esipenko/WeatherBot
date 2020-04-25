import telebot
from telebot import types
import constants
import requests as r
from bs4 import BeautifulSoup as BS

bot = telebot.TeleBot(constants.token)

markup = types.ReplyKeyboardMarkup(True, True)
item1 = types.KeyboardButton("Москва")
item2 = types.KeyboardButton("Санкт-Петербург")
item3 = types.KeyboardButton("Другой город")
markup.add(item1, item2, item3)

moscow = "https://yandex.ru/pogoda/moscow"
spb = "https://yandex.ru/pogoda/saint-petersburg"


def weather(city):
    url = r.get(city)
    soup = BS(url.content, "html.parser")
    res = soup.find("div", class_="temp fact__temp fact__temp_size_s")
    temp = res.find("span", class_="temp__value")
    temp = temp.string.extract() + "°"
    desc = soup.find("div", class_="link__condition day-anchor i-bem")
    desc = desc.string.extract()
    out = temp + ", " + desc
    return out


@bot.message_handler(commands=["start"])
def start_answer(message):
    bot.send_message(message.chat.id, "Привет! Этот бот показывает погоду в вашем городе в реальном времени. \n "
                                      "Выберите город:", reply_markup=markup)


@bot.message_handler(commands=["help"])
def help_answer(message):
    bot.send_message(message.chat.id, "Возникли вопросы? \n Пишите: @Vasily_Esipenko")


@bot.message_handler(content_types=["text"])
def text_answer(message):
    if message.text.lower() in constants.weather_list:
        bot.send_message(message.chat.id, weather(constants.weather_list[message.text.lower()]))
    elif message.text == "Москва":
        bot.send_message(message.chat.id, weather(moscow))
    elif message.text == "Санкт-Петербург":
        bot.send_message(message.chat.id, weather(spb))
    elif message.text == "Другой город":
        bot.send_message(message.chat.id, "Введите название вашего города:")
    else:
        bot.send_message(message.chat.id, "Извините, попробуйте ещё раз")


bot.polling()
