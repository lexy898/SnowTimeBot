import telebot
import logging
import config
from order import order_pages_generator

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')

TOKEN = config.get_token()
_ADMIN_LIST = config.get_admin_list()  # Список chat_id всех админов

bot = telebot.TeleBot(TOKEN)


def send_admin_new_order(order):
    message_to_send = order_pages_generator.admin_create_new_order_page(order)
    for admin in _ADMIN_LIST:
        bot.send_message(admin, message_to_send['message_text'], reply_markup=message_to_send['markup'], parse_mode='HTML')


def send_customer_processing_order(order):
    message_to_send = order_pages_generator.create_order_in_processing_page(order.get_order_id())
    bot.send_message(order.get_chat_id(), message_to_send['message_text'], reply_markup=message_to_send['markup'], parse_mode='HTML')


def send_customer_approve_order(order):
    message_to_send = order_pages_generator.create_order_approved_page(order)
    bot.send_message(order.get_chat_id(), message_to_send['message_text'], reply_markup=message_to_send['markup'], parse_mode='HTML')