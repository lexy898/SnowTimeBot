from telebot import types

import main_menu
import sql_requests


# Создать страницу просмотра единицы инвентаря
def create_item_view_page(item_id):
    message_text = sql_requests.get_url_by_item(item_id)
    markup = types.InlineKeyboardMarkup()
    row = [types.InlineKeyboardButton("Назад", callback_data="back-to-pagination"),
           types.InlineKeyboardButton("Добавить в заказ", callback_data="save-to-preorder" + item_id)]
    markup.row(*row)
    message = {'message_text': message_text, 'markup': markup}
    return message


#  Создать страницу с отображением текущего предзаказа
def create_preorder_page(items_list):
    items_with_attributes = []
    message_text = '<b>Ваш заказ:</b>\n\n'
    markup = types.InlineKeyboardMarkup()

    for item in items_list:
        items_with_attributes.append(sql_requests.get_thing_by_ID(item))  # Подтягиваются параметры предметов
    for item in items_with_attributes:
        if item[1] is not None:
            message_text += '<b>' + item[1].upper() + '</b>\n'
        if item[4] is not None:
            message_text += 'Размер: ' + item[4] + '\n'
        if item[5] is not None:
            message_text += 'Подходит для роста: ' + item[5] + '\n\n'
    row = [types.InlineKeyboardButton("Добавить что-то еще", callback_data="go-to-pagination"),
           types.InlineKeyboardButton("Оформить заказ", callback_data="save-preorder")]
    markup.row(*row)
    row = [types.InlineKeyboardButton("Редактировать заказ", callback_data="edit-preorder")]
    markup.row(*row)
    row = [types.InlineKeyboardButton("Удалить заказ", callback_data="delete-preorder")]
    markup.row(*row)
    message = {'message_text': message_text, 'markup': markup}
    return message


# Создать страницу редактирования предзаказа
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
        row = [types.InlineKeyboardButton("Сохранить", callback_data="go-to-preorder")]
        markup.row(*row)
        row = [types.InlineKeyboardButton("Удалить заказ", callback_data="delete-preorder")]
        markup.row(*row)
        message = {'message_text': message_text, 'markup': markup}
    else:
        message = main_menu.create_main_menu(())
    return message


# создать страницу с подтверждением удаления предзаказа
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
               types.InlineKeyboardButton("Нет", callback_data="go-to-preorder")]
        markup.row(*row)
        message = {'message_text': message_text, 'markup': markup}
    else:
        message = main_menu.create_main_menu({})
    return message


#  Создать страницу с запросом номера телефона
def create_ask_phone_page(customer_phone):
    message_text = ''
    markup = types.InlineKeyboardMarkup()
    if customer_phone is not None:
        message_text += "<b>Ваш телефон: " + customer_phone + "?</b>"
        row = [types.InlineKeyboardButton("Да", callback_data="phone-approved"),
               types.InlineKeyboardButton("Указать другой", callback_data="change-phone-number")]
        markup.row(*row)
        row = [types.InlineKeyboardButton("⬅ Назад", callback_data="go-to-preorder")]
        markup.row(*row)
    else:
        message_text += "Напишите, пожалуйста, Ваш номер для связи\n" \
                        "в формате <b>79xxxxxxxxx</b>"
    message = {'message_text': message_text, 'markup': markup}
    return message


#  Создать страницу с повторным запросом номера, если пользователь ввел номер неправильно
def create_ask_again_phone_page():
    message_text = 'Номер введен неправильно.\n' \
                   'Пожалуйста, попробуйте ввести снова.\n' \
                   'Номер должен быть в формате <b>79xxxxxxxxx</b>'
    markup = types.InlineKeyboardMarkup()
    message = {'message_text': message_text, 'markup': markup}
    return message


#  Создать страничку изменения существующего номера телефона клиента
def create_change_phone_number_page():
    message_text = "Напишите, пожалуйста, Ваш новый номер для связи\n" \
                "в формате <b>79xxxxxxxxx</b>"
    markup = types.InlineKeyboardMarkup()
    row = [types.InlineKeyboardButton("⬅ Назад", callback_data="go-to-preorder")]
    markup.row(*row)
    message = {'message_text': message_text, 'markup': markup}
    return message


#  Создать страничку оформленного заказа
def create_preorder_posted_page():
    markup = types.InlineKeyboardMarkup()
    message_text = 'Спасибо!\n' \
                   'Заказ отправлен.\n' \
                   'Мы свяжемся с вами для подтверждения'
    row = [types.InlineKeyboardButton("Вернуться на главное меню", callback_data="back-to-main-menu")]
    markup.row(*row)
    message = {'message_text': message_text, 'markup': markup}
    return message


#  Создать страничку, предупреждающую о последствиях изменения даты предзаказа
def create_warning_change_date_page():
    message_text = ''
    markup = types.InlineKeyboardMarkup()
    message_text += '<b>Внимание!</b> \n' \
                    'Ваш текущий заказ будет удален.\n' \
                    'На новую дату нужно будет собрать заказ заново'
    row = [types.InlineKeyboardButton("Изменить дату", callback_data="change_preorder_date_approved"),
           types.InlineKeyboardButton("Отмена", callback_data="go-to-pagination")]
    markup.row(*row)
    message = {'message_text': message_text, 'markup': markup}
    return message


