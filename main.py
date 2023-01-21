import requests
import time
import os

import telebot
from telebot import types
from loguru import logger

logger.add('telegram_debug.log', format="{time} {level} {message}",
           level="DEBUG", rotation="10:00", compression=zip
           )
bot = telebot.TeleBot(os.getenv('token_telegram_bot'))
main_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
word_list_button = types.KeyboardButton(text="Добавть токен")
main_keyboard.add(word_list_button)
BASE_PATH = 'http://127.0.0.1:8090'


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет', reply_markup=main_keyboard)

@logger.catch
def check_telegram_token(token):
    data = {'telegram_token': token.text, 'chat_id': token.chat.id}
    res = requests.post(f'{BASE_PATH}/api/v1/messages/check_telegram_token/', json=data)
    bot.send_message(token.chat.id, res)
    return res


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'Добавть токен':
        try:
            send_telegram_token = bot.send_message(message.chat.id, 'Введите токен полученный от сервиса')
            bot.register_next_step_handler(send_telegram_token, check_telegram_token)
        except Exception as e:
            logger.debug(f'error add token {e}')


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print('error', e)
        logger.debug(f'error bot polling {e}')
        time.sleep(15)
