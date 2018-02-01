from telebot import types

import sql_requests


def create_new_order_page(order):
    order_items = order['ITEM_LIST']
    message_text = '<b>Новый заказ на:' + order['START_DATE'] + '</b>\n\n'
    # message_text = 'Номер заказа:<b>#' + order['ORDER_ID'] + '</b>\n\n'
    markup = types.InlineKeyboardMarkup()
    items_with_attributes = []

    for item in order_items:
        items_with_attributes.append(sql_requests.get_thing_by_ID(item)) # Подтягиваются названия предметов
    for item in items_with_attributes:
        if item[1] is not None:
            message_text += '<b>🚩' + item[1].upper() + '</b>\n'
    message_text += '\n\n<b>Номер телефона: </b>' + order['PHONE']
    row = [types.InlineKeyboardButton("Подтвердить", callback_data="order_approved"),
           types.InlineKeyboardButton("Отменить", callback_data="order_not_approved")]
    markup.row(*row)
    message = {'message_text': message_text, 'markup': markup}
    return message
