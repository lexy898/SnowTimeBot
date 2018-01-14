from telebot import types

import main_menu
import sql_requests


def create_preorder_page(items_list):
    preorder_items = []
    message_text = '<b>Ваш заказ:</b>\n\n'
    markup = types.InlineKeyboardMarkup()

    for item in items_list:
        preorder_items.append(sql_requests.get_thing_by_ID(item))
    for item in preorder_items:
        if item[1] is not None:
            message_text += '<b>' + item[1].upper() + '</b>\n'
        if item[4] is not None:
            message_text += 'Размер: ' + item[4] + '\n'
        if item[5] is not None:
            message_text += 'Подходит для роста: ' + item[5] + '\n\n'
    row = [types.InlineKeyboardButton("Добавить что-то еще", callback_data="add-to-preorder"),
           types.InlineKeyboardButton("Оформить заказ", callback_data="save-preorder")]
    markup.row(*row)
    row = [types.InlineKeyboardButton("Редактировать заказ", callback_data="edit-preorder")]
    markup.row(*row)
    row = [types.InlineKeyboardButton("Удалить заказ", callback_data="delete-preorder")]
    markup.row(*row)
    message = {'message_text': message_text, 'markup': markup}
    return message


def create_edit_preorder_page(items_list):
    if items_list:
        preorder_items = []
        message_text = '<b>Ваш заказ(РЕДАКТИРОВАНИЕ):</b>\n\n'
        markup = types.InlineKeyboardMarkup()

        for item in items_list:
            preorder_items.append(sql_requests.get_thing_by_ID(item))
        for item in preorder_items:
            if item[1] is not None:
                message_text += '<b>' + item[1].upper() + '</b>\n'
            if item[4] is not None:
                message_text += 'Размер: ' + item[4] + '\n'
            if item[5] is not None:
                message_text += 'Подходит для роста: ' + item[5] + '\n'
            message_text += '<b>Удалить из заказа:</b> /delete_from_preorder_' + str(item[0]) + '\n\n'
            #  callback_data используется аналогичная кнопке "нет" при отмене удаления предзаказа
        row = [types.InlineKeyboardButton("Сохранить", callback_data="delete-preorder-no")]
        markup.row(*row)
        row = [types.InlineKeyboardButton("Удалить заказ", callback_data="delete-preorder")]
        markup.row(*row)
        message = {'message_text': message_text, 'markup': markup}
    else:
        message = main_menu.create_main_menu()
    return message


def create_delete_approve_page(items_list):
    if items_list:
        preorder_items = []
        message_text = '<b>ВЫ ДЕЙСТВИТЕЛЬНО ХОТИТЕ УДАЛИТЬ СВОЙ ЗАКАЗ?</b>\n\n'
        markup = types.InlineKeyboardMarkup()

        for item in items_list:
            preorder_items.append(sql_requests.get_thing_by_ID(item))
        for item in preorder_items:
            if item[1] is not None:
                message_text += '<b>' + item[1].upper() + '</b>\n'
            if item[4] is not None:
                message_text += 'Размер: ' + item[4] + '\n'
            if item[5] is not None:
                message_text += 'Подходит для роста: ' + item[5] + '\n\n'

        row = [types.InlineKeyboardButton("Да", callback_data="delete-preorder-yes"),
               types.InlineKeyboardButton("Нет", callback_data="delete-preorder-no")]
        markup.row(*row)
        message = {'message_text': message_text, 'markup': markup}
    else:
        message = main_menu.create_main_menu()
    return message