import os
from urllib import request
import telebot
import pytaf

TOKEN = os.environ.get('TOKEN')
URL_METAR = "https://tgftp.nws.noaa.gov/data/observations/metar/stations/UUWW.TXT"
URL_TAF = "https://tgftp.nws.noaa.gov/data/forecasts/taf/stations/UUWW.TXT"

bot = telebot.TeleBot(token=TOKEN, threaded=False)
keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row('/start', '/get_metar', '/get_taf')


def start(message):
    msg = "Привет. Это бот для получения авиационного прогноза погоды " \
          "с серверов NOAA. Бот настроен на аэропорт Внуково (UUWW)."
    bot.send_message(message.chat.id, msg, reply_markup=keyboard)


def parse_data(code):
    code = code.split('\n')[1]
    return pytaf.Decoder(pytaf.TAF(code)).decode_taf()


def get_metar(message):
    # Fetch info from server.
    code = request.urlopen(URL_METAR).read().decode('utf-8')
    # Send formatted answer.
    bot.send_message(message.chat.id, parse_data(code), reply_markup=keyboard)


def get_taf(message):
    # Fetch info from server.
    code = request.urlopen(URL_TAF).read().decode('utf-8')
    # Send formatted answer.
    bot.send_message(message.chat.id, parse_data(code), reply_markup=keyboard)


def route_command(command, message):
    """
    Commands router.
    """
    if command == '/start':
        return start(message)
    elif command == '/get_metar':
        return get_metar(message)
    elif command == '/get_taf':
        return get_taf(message)


def main(**kwargs):
    """
    Serverless environment entry point.
    """
    print(f'Received: "{kwargs}"')
    message = telebot.types.Update.de_json(kwargs)
    message = message.message or message.edited_message
    if message and message.text and message.text[0] == '/':
        print(f'Echo on "{message.text}"')
        route_command(message.text.lower(), message)
