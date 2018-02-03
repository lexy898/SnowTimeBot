import telebot
import logging
import config
from order import order_pages_generator

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')

TOKEN = config.get_token()
_ADMIN_LIST = config.get_admin_list()  # Список chat_id всех админов

bot = telebot.TeleBot(TOKEN)


def send_admin_new_order(order):
    message_to_send = order_pages_generator.create_new_order_page(order)
    for admin in _ADMIN_LIST:
        bot.send_message(admin, message_to_send['message_text'], reply_markup=message_to_send['markup'], parse_mode='HTML')

