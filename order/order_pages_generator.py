from datetime import datetime

from telebot import types

import sql_requests


def _new_order_page(order):
    order_items = order.get_item_list()
    start_date = datetime.strptime(order.get_start_date(), "%Y-%m-%d %H:%M:%S")
    start_date = datetime.strftime(start_date, "%d-%m-%Y")
    message_text = 'Номер заказа: <b>#' + order.get_order_id() + '</b>\n'
    message_text += 'На дату: <b>' + start_date + '</b>\n\n'
    items_with_attributes = []

    for item in order_items:
        items_with_attributes.append(sql_requests.get_thing_by_ID(item))  # Подтягиваются названия предметов
    for item in items_with_attributes:
        if item[1] is not None:
            message_text += '<b>🚩[id' + str(item[0]) + "] " + item[1].upper() + '</b>\n'
    if order.get_discount() is not None and order.get_discount() > 0:
        message_text += '\nСумма: ' + str(order.get_price()) + 'Р.\n'
        message_text += 'Скидка за комплект: ' + str(order.get_discount()) + 'Р.\n'
        message_text += '<b>Итого: ' + str(order.get_actual_price()) + 'Р.</b>\n'
    else:
        message_text += '\n<b>Итого: ' + str(order.get_actual_price()) + 'Р.</b>\n'
    message_text += '\n<b>Номер телефона: </b>' + order.get_phone()
    return message_text


'''
*************************************************
************* СТРАНИЧКИ ДЛЯ АДМИНИСТРАТОРА*******
*************************************************
'''


def admin_create_new_order_page(order):
    message_text = '<b>⭐Новый заказ!</b>\n'
    message_text += _new_order_page(order)
    markup = types.InlineKeyboardMarkup()
    row = [types.InlineKeyboardButton("Взять в работу", callback_data="processing-order" + order.get_order_id()),
           types.InlineKeyboardButton("Отменить", callback_data="order-not-approved" + order.get_order_id())]
    markup.row(*row)
    message = {'message_text': message_text, 'markup': markup}
    return message


def admin_create_order_in_processing_page(order):
    message_text = '<b> Заказ взят в работу</b>\n'
    message_text += _new_order_page(order)
    markup = types.InlineKeyboardMarkup()
    row = [types.InlineKeyboardButton("Подтвердить", callback_data="approve-order" + order.get_order_id()),
           types.InlineKeyboardButton("Отменить", callback_data="order-not-approved" + order.get_order_id())]
    markup.row(*row)
    message = {'message_text': message_text, 'markup': markup}
    return message


def admin_create_order_approved_page(order):
    message_text = '<b> Заказ #' + str(order.get_order_id()) + ' подтвержден</b>\n'
    markup = types.InlineKeyboardMarkup()
    row = [types.InlineKeyboardButton("На главное меню", callback_data="go-to-admin-menu")]
    markup.row(*row)
    message = {'message_text': message_text, 'markup': markup}
    return message


def admin_create_is_not_admin_page():
    message_text = "У Вас нет прав администратора"
    markup = types.InlineKeyboardMarkup()
    row = [types.InlineKeyboardButton("На главное меню", callback_data="go-to-admin-menu")]
    markup.row(*row)
    message = {'message_text': message_text, 'markup': markup}
    return message


def admin_create_order_canceled_page(order_id):
    message_text = '<b> Заказ #' + str(order_id) + ' отменен</b>\n'
    markup = types.InlineKeyboardMarkup()
    row = [types.InlineKeyboardButton("На главное меню", callback_data="go-to-admin-menu")]
    markup.row(*row)
    message = {'message_text': message_text, 'markup': markup}
    return message


#  Страничка сообщает о том, что заказ обрабатывается другим администратором
def admin_create_order_unavailable_page(admin, order_id):
    message_text = 'Заказ <b>#' + str(order_id) + '</b> обрабатывается другим администратором\n'
    message_text += 'Админ: <b>' + admin.admin_name + '</b>\n'
    message_text += 'Телефон: <b>' + admin.admin_phone + '</b>\n'
    markup = types.InlineKeyboardMarkup()
    row = [types.InlineKeyboardButton("На главное меню", callback_data="go-to-admin-menu")]
    markup.row(*row)
    message = {'message_text': message_text, 'markup': markup}
    return message


'''
*************************************************
************* СТРАНИЧКИ ДЛЯ КЛИЕНТА*******
*************************************************
'''


def create_order_in_processing_page(order_id):
    message_text = '<b>⭐Ваш заказ #' + str(order_id) + ' взят в работу</b>\n'
    markup = types.InlineKeyboardMarkup()
    row = [types.InlineKeyboardButton("Вернуться на главное меню", callback_data="back-to-main-menu")]
    markup.row(*row)
    message = {'message_text': message_text, 'markup': markup}
    return message


def create_order_approved_page(order):
    start_date = datetime.strptime(order.get_start_date(), "%Y-%m-%d %H:%M:%S")
    start_date = datetime.strftime(start_date, "%d-%m-%Y")
    message_text = '<b>⭐Ваш заказ #' + str(order.get_order_id()) + ' подтвержден!</b>\n'
    message_text += 'Ждем Вас <b>' + start_date + '</b> по адресу: ул.Благовещенская 69, Вологда.\n'
    message_text += 'Сумма заказа: <b>' + str(order.get_actual_price()) + '</b>'
    markup = types.InlineKeyboardMarkup()
    row = [types.InlineKeyboardButton("Вернуться на главное меню", callback_data="back-to-main-menu")]
    markup.row(*row)
    message = {'message_text': message_text, 'markup': markup}
    return message

