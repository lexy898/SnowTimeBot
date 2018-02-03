from telebot import types

import sql_requests


def create_new_order_page(order):
    order_items = order.get_item_list()
    message_text = '<b>Новый заказ на:' + order.get_start_date() + '</b>\n\n'
    markup = types.InlineKeyboardMarkup()
    items_with_attributes = []

    for item in order_items:
        items_with_attributes.append(sql_requests.get_thing_by_ID(item)) # Подтягиваются названия предметов
    for item in items_with_attributes:
        if item[1] is not None:
            message_text += '<b>🚩' + item[1].upper() + '</b>\n'
    message_text += '\n\n<b>Номер телефона: </b>' + order.get_phone()
    row = [types.InlineKeyboardButton("Взять в работу", callback_data="processing-order"),
           types.InlineKeyboardButton("Отменить", callback_data="order_not_approved")]
    markup.row(*row)
    message = {'message_text': message_text, 'markup': markup}
    return message
