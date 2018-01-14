import datetime

import sys
import telebot
import logging
import config
import main_menu
import preorder
import sql_requests
from telegramcalendar import create_calendar
import pagination
from telebot import types

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')

TOKEN = config.get_token()

bot = telebot.TeleBot(TOKEN)

current_shown_dates = {}  # Текущая дата, закрепленная за пользователем
current_type_of_thing = {}  # Текущий тип вещи, закрепленный за пользователем
current_page = {}  # Текущая страница, закрепленная за пользователем
preorders_list = {}  # Список предзаказов пользователей(корзины)


# Создание главного меню
@bot.message_handler(commands=['menu'])
def get_main_menu(message):
    chat_id = message.chat.id
    try:
        preorder = preorders_list[chat_id]
    except KeyError:
        preorder = []
    message_to_send = main_menu.create_main_menu(preorder)
    bot.send_sticker(chat_id, 'CAADAgADAgAD2INrCdsC2_uAN23lAg')
    bot.send_message(chat_id, message_to_send['message_text'], reply_markup=message_to_send['markup'])


#  Переход на главное меню
@bot.callback_query_handler(func=lambda call: call.data == 'back-to-main-menu')
def get_main_menu_from_outside(call):
    chat_id = call.message.chat.id
    try:
        preorder = preorders_list[chat_id]
    except KeyError:
        preorder = []
    message = main_menu.create_main_menu(preorder)
    bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                          reply_markup=message['markup'])


#  Открыть выбранный item
@bot.message_handler(content_types=['text'])
def open_item(message):
    chat_id = message.chat.id
    try:
        if '/item' in message.text:
            item_number = message.text[6:]
            message_text = sql_requests.get_url_by_item(item_number)
            markup = types.InlineKeyboardMarkup(row_width=1)
            row = [types.InlineKeyboardButton("Назад", callback_data="back-to-pagination"),
                   types.InlineKeyboardButton("Добавить в заказ", callback_data="save-to-preorder" + item_number)]
            markup.row(*row)
            bot.send_message(chat_id, message_text, reply_markup=markup)
        if '/delete_from_preorder' in message.text:
            item_number = message.text[22:]
            preorder_items = preorders_list[chat_id]
            preorder_items.remove(item_number)
            preorders_list[chat_id] = preorder_items
            message = preorder.create_edit_preorder_page(preorders_list[chat_id])
            bot.send_message(chat_id, message['message_text'], reply_markup=message['markup'], parse_mode='HTML')
    except KeyError as err:
        get_main_menu(message)
        logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
    except ValueError as err:
        get_main_menu(message)
        logging.error(u'Method:' + sys._getframe().f_code.co_name + ' ValueError: ' + str(err) + '')


'''
*************************************************
*************КАЛЕНДАРЬ***************************
*************************************************
'''


@bot.callback_query_handler(func=lambda call: call.data[0:9] == 'main_menu')
def get_calendar(call):
    now = datetime.datetime.now()  # Current date
    chat_id = call.message.chat.id
    global current_type_of_thing
    current_type_of_thing[chat_id] = call.data[15:].upper()
    date = (now.year, now.month)
    current_shown_dates[chat_id] = date  # Saving the current date in a dict
    markup = create_calendar(now.year, now.month)
    bot.edit_message_text("Пожалуйста, Выберите дату, на которую хотите взять прокат", call.from_user.id,
                          call.message.message_id, reply_markup=markup)
    bot.answer_callback_query(call.id, text="")


@bot.callback_query_handler(func=lambda call: call.data[0:13] == 'calendar-day-')
def get_day(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    current_page[chat_id] = 0
    if saved_date is not None:
        #  day = call.data[13:]
        #  date = datetime.datetime(int(saved_date[0]), int(saved_date[1]), int(day), 0, 0, 0)
        #  bot.send_message(chat_id, str(date))
        message = pagination.create_list(current_type_of_thing.get(chat_id), 0)
        bot.edit_message_text(message['message_text'], call.from_user.id,
                              call.message.message_id, reply_markup=message['markup'], parse_mode='HTML')
        bot.answer_callback_query(call.id, text="")
    else:
        # Do something to inform of the error
        bot.answer_callback_query(call.id, text="Время выбора даты истекло")
        get_main_menu(call.message)
        pass


@bot.callback_query_handler(func=lambda call: call.data == 'next-month')
def next_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if saved_date is not None:
        year, month = saved_date
        month += 1
        if month > 12:
            month = 1
            year += 1
        date = (year, month)
        current_shown_dates[chat_id] = date
        markup = create_calendar(year, month)
        bot.edit_message_text("Пожалуйста, Выберите дату, на которую хотите взять прокат", call.from_user.id,
                              call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        # Do something to inform of the error
        bot.answer_callback_query(call.id, text="Время выбора даты истекло")
        get_main_menu(call.message)
        pass


@bot.callback_query_handler(func=lambda call: call.data == 'previous-month')
def previous_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if saved_date is not None:
        year, month = saved_date
        month -= 1
        if month < 1:
            month = 12
            year -= 1
        date = (year, month)
        current_shown_dates[chat_id] = date
        markup = create_calendar(year, month)
        bot.edit_message_text("Пожалуйста, Выберите дату, на которую хотите взять прокат", call.from_user.id,
                              call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        # Do something to inform of the error
        bot.answer_callback_query(call.id, text="Время выбора даты истекло")
        get_main_menu(call.message)
        pass


@bot.callback_query_handler(func=lambda call: call.data == 'ignore')
def ignore(call):
    bot.answer_callback_query(call.id, text="")


'''
*************************************************
*************ПАГИНАЦИЯ***************************
*************************************************
'''


@bot.callback_query_handler(func=lambda call: call.data == 'next-page')
def next_page(call):
    current_page[call.message.chat.id] = turn_page(call)


@bot.callback_query_handler(func=lambda call: call.data == 'previous-page')
def previous_page(call):
    current_page[call.message.chat.id] = turn_page(call)


@bot.callback_query_handler(func=lambda call: call.data == 'back-to-pagination')
def previous_page_from_item_page(call):
    chat_id = call.message.chat.id
    try:
        message = pagination.create_list(current_type_of_thing.get(chat_id), current_page[chat_id])
        bot.edit_message_text(message['message_text'], call.from_user.id,
                              call.message.message_id, reply_markup=message['markup'], parse_mode='HTML')
        bot.answer_callback_query(call.id, text="")
    except KeyError as err:
        bot.answer_callback_query(call.id, text="Что-то пошло не так. Попробуйте, пожалуйста, снова.")
        get_main_menu(call.message)
        logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')


def turn_page(call):
    try:
        chat_id = call.message.chat.id
        if call.data == 'next-page':
            current_page[chat_id] += 1
        else:
            current_page[chat_id] -= 1
        message = pagination.create_list(current_type_of_thing.get(chat_id), current_page[chat_id])
        bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                              reply_markup=message['markup'], parse_mode='HTML')
        bot.answer_callback_query(call.id, text="")
        return current_page[chat_id]
    except KeyError as err:
        logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
        get_main_menu_from_outside(call)
        return 0


'''
*************************************************
*************РАБОТА С  ПРЕДЗАКАЗОМ***************************
*************************************************
'''


# Сохранить вещь в предзаказ
@bot.callback_query_handler(func=lambda call: call.data[0:16] == 'save-to-preorder')
def save_to_preorder(call):
    chat_id = call.message.chat.id
    item_number = call.data[16:]
    try:
        preorder_item_list = preorders_list[chat_id]
        preorder_item_list.append(item_number)
        preorders_list[chat_id] = preorder_item_list
    except KeyError:
        preorder_item_list = [item_number]
        preorders_list[chat_id] = preorder_item_list
    message = preorder.create_preorder_page(preorders_list[chat_id])
    bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                          reply_markup=message['markup'], parse_mode='HTML')
    bot.answer_callback_query(call.id, text="Добавлено")


#  добавить в предзаказ что-нибудь еще
@bot.callback_query_handler(func=lambda call: call.data == 'add-to-preorder')
def add_to_preorder(call):
    previous_page_from_item_page(call)


#  Сохранить предзаказ(создание заказа)
@bot.callback_query_handler(func=lambda call: call.data == 'save-preorder')
def save_preorder(call):
    previous_page_from_item_page(call)


# Редактировать предзаказ
@bot.callback_query_handler(func=lambda call: call.data == 'edit-preorder')
def edit_preorder(call):
    chat_id = call.message.chat.id
    message = preorder.create_edit_preorder_page(preorders_list[chat_id])
    bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                          reply_markup=message['markup'], parse_mode='HTML')
    bot.answer_callback_query(call.id, text="")


#  Удалить предзаказ. Появляется страничка одтверждения
@bot.callback_query_handler(func=lambda call: call.data == 'delete-preorder')
def delete_preorder(call):
    try:
        chat_id = call.message.chat.id
        message = preorder.create_delete_approve_page(preorders_list[chat_id])
        bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                              reply_markup=message['markup'], parse_mode='HTML')
        bot.answer_callback_query(call.id, text="")
    except KeyError as err:
        bot.answer_callback_query(call.id, text="Что-то пошло не так. Попробуйте, пожалуйста, снова.")
        get_main_menu(call.message)
        logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')


#  Подтверждение удаления заказа
@bot.callback_query_handler(func=lambda call: call.data == 'delete-preorder-yes')
def delete_preorder_yes(call):
    try:
        chat_id = call.message.chat.id
        del preorders_list[chat_id]
        message = main_menu.create_main_menu(())
        bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                              reply_markup=message['markup'], parse_mode='HTML')
        bot.answer_callback_query(call.id, text="Заказ успешно удален")
    except KeyError as err:
        bot.answer_callback_query(call.id, text="Что-то пошло не так. Попробуйте, пожалуйста, снова.")
        get_main_menu(call.message)
        logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')


#  Отмена удаления заказа
@bot.callback_query_handler(func=lambda call: call.data == 'delete-preorder-no')
def delete_preorder_no(call):
    try:
        chat_id = call.message.chat.id
        message = preorder.create_preorder_page(preorders_list[chat_id])
        bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                              reply_markup=message['markup'], parse_mode='HTML')
        bot.answer_callback_query(call.id, text="")
    except KeyError as err:
        bot.answer_callback_query(call.id, text="Что-то пошло не так. Попробуйте, пожалуйста, снова.")
        get_main_menu(call.message)
        logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')




bot.polling(none_stop=True, interval=0)
