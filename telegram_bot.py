import datetime
import sys
import telebot
import logging
import config
import main_menu
from order import order_management
from preorder import preorder_management
from preorder import preorder_pages_generator
from telegramcalendar import create_calendar
import pagination
from customer import customer_management
import input_validator
import time

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')

TOKEN = config.get_token()

bot = telebot.TeleBot(TOKEN)

order_mngmnt = order_management.OrderManagement()  # Управление Заказами
customer_mngmnt = customer_management.CustomerManagement()  # управление клиентами
preorder_mngmnt = preorder_management.PreorderManagement()  # Управление предзаказамиф
input_validate = input_validator.InputValidator()

customer_mngmnt.init_customers()


#  Обработка ошибок
def key_error_handler(err, call):
    bot.answer_callback_query(call.id, text="Что-то пошло не так. Попробуйте, пожалуйста, снова.")
    get_main_menu_from_outside(call)
    logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')


#  Обработка ошибок
def value_error_handler(err, call):
    bot.answer_callback_query(call.id, text="Что-то пошло не так. Попробуйте, пожалуйста, снова.")
    get_main_menu_from_outside(call)
    logging.error(u'Method:' + sys._getframe().f_code.co_name + ' ValueError: ' + str(err) + '')


#  Обработка ошибок
def attribute_error_handler(err, call):
    bot.answer_callback_query(call.id, text="Что-то пошло не так. Попробуйте, пожалуйста, снова.")
    get_main_menu_from_outside(call)
    logging.error(u'Method:' + sys._getframe().f_code.co_name + ' AttributeError: ' + str(err) + '')


def type_error_handler(err, call):
    bot.answer_callback_query(call.id, text="Что-то пошло не так. Попробуйте, пожалуйста, снова.")
    get_main_menu_from_outside(call)
    logging.error(u'Method:' + sys._getframe().f_code.co_name + ' TypeError: ' + str(err) + '')


# Создание главного меню
@bot.message_handler(commands=['start'])
def get_main_menu(message):
    chat_id = message.chat.id
    if not customer_mngmnt.check_existence_client(chat_id):
        customer_mngmnt.add_new_customer(message)
    message_to_send = main_menu.create_main_menu(preorder_mngmnt.get_preorder(chat_id))
    bot.send_sticker(chat_id, 'CAADAgADAgAD2INrCdsC2_uAN23lAg')
    bot.send_message(chat_id, message_to_send['message_text'], reply_markup=message_to_send['markup'])
    input_validate.off_input_phone_mode(chat_id)  # Отключаем режим ввода телефона


#  Переход на главное меню
@bot.callback_query_handler(func=lambda call: call.data == 'back-to-main-menu')
def get_main_menu_from_outside(call):
    try:
        chat_id = call.message.chat.id
        preorder = preorder_mngmnt.get_preorder(chat_id)
        message = main_menu.create_main_menu(preorder)
        bot.send_sticker(chat_id, 'CAADAgADAgAD2INrCdsC2_uAN23lAg')
        bot.send_message(chat_id, message['message_text'], reply_markup=message['markup'])
        input_validate.off_input_phone_mode(str(chat_id))  # Отключаем режим ввода телефона
    except AttributeError as err:
        attribute_error_handler(err, call)
    except KeyError as err:
        key_error_handler(err, call)


#  Открыть выбранный item / удалить вещь из предзаказа
@bot.message_handler(content_types=['text'])
def open_item(message):
    chat_id = message.chat.id
    message_to_send = {}
    try:
        if '/item' in message.text:
            item_id = message.text[6:]
            message_to_send.update(preorder_pages_generator.create_item_view_page(item_id))
        elif '/delete_from_preorder' in message.text:
            item_id = message.text[22:]
            preorder_mngmnt.remove_item(chat_id, item_id)
            message_to_send.update(
                preorder_pages_generator.create_edit_preorder_page(preorder_mngmnt.get_preorder(chat_id).get_item_list()))
        elif input_validate.check_input_phone_mode(chat_id):
            if input_validate.validation_phone(message.text):
                message_to_send.update(preorder_pages_generator.create_preorder_posted_page())
                customer_mngmnt.update_customer_phone(chat_id, message.text)
                preorder_mngmnt.get_preorder(chat_id).set_phone(message.text)
                order_mngmnt.create_order(preorder_mngmnt.get_preorder(chat_id))
            else:
                message_to_send.update(preorder_pages_generator.create_ask_again_phone_page())
        bot.send_message(chat_id, message_to_send['message_text'], reply_markup=message_to_send['markup'],
                         parse_mode='HTML')
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
    try:
        chat_id = call.message.chat.id
        customer_mngmnt.get_customer(chat_id).set_current_type_of_thing(call.data[15:].upper())
        if not preorder_mngmnt.is_preorder_exist(chat_id):
            now = datetime.datetime.now()  # Current date
            date = (now.year, now.month)
            customer_mngmnt.get_customer(chat_id).set_current_calendar_month(date) # Saving the current date in a dict
            markup = create_calendar(now.year, now.month)
            bot.edit_message_text("Пожалуйста, выберите дату, на которую планируете взять прокат", call.from_user.id,
                                  call.message.message_id, reply_markup=markup)
            bot.answer_callback_query(call.id, text="")
        else:
            message = pagination.create_list(customer_mngmnt.get_customer(chat_id).get_current_type_of_thing(), 0,
                                             preorder_mngmnt.get_preorder(chat_id).get_start_date())
            bot.edit_message_text(message['message_text'], call.from_user.id,
                                  call.message.message_id, reply_markup=message['markup'], parse_mode='HTML')
            bot.answer_callback_query(call.id, text="")
    except AttributeError as err:
        attribute_error_handler(err, call)


@bot.callback_query_handler(func=lambda call: call.data[0:13] == 'calendar-day-')
def get_day(call):
    try:
        chat_id = call.message.chat.id
        saved_date = customer_mngmnt.get_customer(chat_id).get_current_calendar_month()
        customer_mngmnt.get_customer(chat_id).set_current_page(0)
        if saved_date is not None:
            day = call.data[13:]
            date = str(datetime.datetime(int(saved_date[0]), int(saved_date[1]), int(day), 0, 0, 0))
            preorder_mngmnt.create_preorder(chat_id, date)
            message = pagination.create_list(customer_mngmnt.get_customer(chat_id).get_current_type_of_thing(), 0,
                                             preorder_mngmnt.get_preorder(chat_id).get_start_date())
            bot.edit_message_text(message['message_text'], call.from_user.id,
                                  call.message.message_id, reply_markup=message['markup'], parse_mode='HTML')
            bot.answer_callback_query(call.id, text="")
        else:
            # Do something to inform of the error
            bot.answer_callback_query(call.id, text="Время выбора даты истекло")
            get_main_menu(call.message)
    except AttributeError as err:
        attribute_error_handler(err, call)


@bot.callback_query_handler(func=lambda call: call.data == 'next-month')
def next_month(call):
    chat_id = call.message.chat.id
    saved_date = customer_mngmnt.get_customer(chat_id).get_current_calendar_month()
    if saved_date is not None:
        year, month = saved_date
        month += 1
        if month > 12:
            month = 1
            year += 1
        date = (year, month)
        customer_mngmnt.get_customer(chat_id).set_current_calendar_month(date)
        markup = create_calendar(year, month)
        bot.edit_message_text("Пожалуйста, Выберите дату, на которую хотите взять прокат", call.from_user.id,
                              call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        # Do something to inform of the error
        bot.answer_callback_query(call.id, text="Время выбора даты истекло")
        get_main_menu(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'previous-month')
def previous_month(call):
    chat_id = call.message.chat.id
    saved_date = customer_mngmnt.get_customer(chat_id).get_current_calendar_month()
    if saved_date is not None:
        year, month = saved_date
        month -= 1
        if month < 1:
            month = 12
            year -= 1
        date = (year, month)
        customer_mngmnt.get_customer(chat_id).set_current_calendar_month(date)
        markup = create_calendar(year, month)
        bot.edit_message_text("Пожалуйста, Выберите дату, на которую хотите взять прокат", call.from_user.id,
                              call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        # Do something to inform of the error
        bot.answer_callback_query(call.id, text="Время выбора даты истекло")
        get_main_menu(call.message)


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
    customer_mngmnt.get_customer(call.message.chat.id).set_current_page(turn_page(call))


@bot.callback_query_handler(func=lambda call: call.data == 'previous-page')
def previous_page(call):
    customer_mngmnt.get_customer(call.message.chat.id).set_current_page(turn_page(call))


@bot.callback_query_handler(func=lambda call: call.data == 'back-to-pagination')
def previous_page_from_item_page(call):
    chat_id = call.message.chat.id
    try:
        message = pagination.create_list(customer_mngmnt.get_customer(chat_id).get_current_type_of_thing(),
                                         customer_mngmnt.get_customer(chat_id).get_current_page(),
                                         preorder_mngmnt.get_preorder(chat_id).get_start_date())
        bot.edit_message_text(message['message_text'], call.from_user.id,
                              call.message.message_id, reply_markup=message['markup'], parse_mode='HTML')
        bot.answer_callback_query(call.id, text="")
    except KeyError as err:
        key_error_handler(err, call)
    except AttributeError as err:
        attribute_error_handler(err, call)


def turn_page(call):
    try:
        chat_id = call.message.chat.id
        current_page = customer_mngmnt.get_customer(chat_id).get_current_page()
        if call.data == 'next-page':
            customer_mngmnt.get_customer(chat_id).set_current_page(current_page + 1)
        else:
            customer_mngmnt.get_customer(chat_id).set_current_page(current_page - 1)
        current_page = customer_mngmnt.get_customer(chat_id).get_current_page()
        message = pagination.create_list(customer_mngmnt.get_customer(chat_id).get_current_type_of_thing(),
                                         current_page, preorder_mngmnt.get_preorder(chat_id).get_start_date())
        bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                              reply_markup=message['markup'], parse_mode='HTML')
        bot.answer_callback_query(call.id, text="")
        return current_page
    except KeyError as err:
        key_error_handler(err, call)
        return 0
    except AttributeError as err:
        attribute_error_handler(err, call)
        return 0
    except TypeError as err:
        type_error_handler(err, call)
        return 0

'''
*************************************************
*************РАБОТА С  ПРЕДЗАКАЗОМ***************************
*************************************************
'''


# Сохранить вещь в предзаказ
@bot.callback_query_handler(func=lambda call: call.data[0:16] == 'save-to-preorder')
def save_to_preorder(call):
    try:
        chat_id = call.message.chat.id
        item_id = call.data[16:]
        preorder_mngmnt.get_preorder(chat_id).add_item(item_id)
        message = preorder_pages_generator.create_preorder_page(preorder_mngmnt.get_preorder(chat_id))
        bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                              reply_markup=message['markup'], parse_mode='HTML')
        bot.answer_callback_query(call.id, text="Добавлено")
    except AttributeError as err:
        attribute_error_handler(err, call)
    except KeyError as err:
        key_error_handler(err, call)


#  Открыть страничку пагинации с выбором инвентаря
@bot.callback_query_handler(func=lambda call: call.data == 'go-to-pagination')
def go_to_pagination(call):
    previous_page_from_item_page(call)


#  Сохранить предзаказ(создание заказа)
@bot.callback_query_handler(func=lambda call: call.data == 'save-preorder')
def save_preorder(call):
    try:
        chat_id = call.message.chat.id
        input_validate.set_input_phone_mode(chat_id)  # Включаем режим ввода телефона
        message = preorder_pages_generator.create_ask_phone_page(customer_mngmnt.get_customer(chat_id).get_phone())
        bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                              reply_markup=message['markup'], parse_mode='HTML')
        bot.answer_callback_query(call.id, text="")
    except AttributeError as err:
        attribute_error_handler(err, call)
    except KeyError as err:
        key_error_handler(err, call)


# Редактировать предзаказ
@bot.callback_query_handler(func=lambda call: call.data == 'edit-preorder')
def edit_preorder(call):
    try:
        chat_id = call.message.chat.id
        message = preorder_pages_generator.create_edit_preorder_page(preorder_mngmnt.get_preorder(chat_id).get_item_list())
        bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                              reply_markup=message['markup'], parse_mode='HTML')
        bot.answer_callback_query(call.id, text="")
    except AttributeError as err:
        attribute_error_handler(err, call)
    except KeyError as err:
        key_error_handler(err, call)


#  Удалить предзаказ. Появляется страничка подтверждения
@bot.callback_query_handler(func=lambda call: call.data == 'delete-preorder')
def delete_preorder(call):
    try:
        chat_id = call.message.chat.id
        message = preorder_pages_generator.create_delete_approve_page(preorder_mngmnt.get_preorder(chat_id).get_item_list())
        bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                              reply_markup=message['markup'], parse_mode='HTML')
        bot.answer_callback_query(call.id, text="")
    except AttributeError as err:
        attribute_error_handler(err, call)
    except KeyError as err:
        key_error_handler(err, call)


#  Подтверждение удаления заказа
@bot.callback_query_handler(func=lambda call: call.data == 'delete-preorder-yes')
def delete_preorder_yes(call):
    try:
        chat_id = call.message.chat.id
        preorder_mngmnt.remove_preorder(chat_id)
        get_main_menu(call.message)
        bot.answer_callback_query(call.id, text="Заказ успешно удален")
    except AttributeError as err:
        attribute_error_handler(err, call)
    except KeyError as err:
        key_error_handler(err, call)


#  Отмена удаления предзаказа
@bot.callback_query_handler(func=lambda call: call.data == 'go-to-preorder')
def go_to_preorder(call):
    try:
        chat_id = call.message.chat.id
        message = preorder_pages_generator.create_preorder_page(preorder_mngmnt.get_preorder(chat_id))
        bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                              reply_markup=message['markup'], parse_mode='HTML')
        bot.answer_callback_query(call.id, text="")
        input_validate.off_input_phone_mode(chat_id)  # Отключаем режим ввода телефона
    except AttributeError as err:
        attribute_error_handler(err, call)
    except KeyError as err:
        key_error_handler(err, call)


#  Телефон изменять не нужно
@bot.callback_query_handler(func=lambda call: call.data == 'phone-approved')
def phone_approved(call):
    try:
        customer_phone = customer_mngmnt.get_customer(call.message.chat.id).get_phone()
        preorder_mngmnt.get_preorder(call.message.chat.id).set_phone(customer_phone)
        if order_mngmnt.create_order(preorder_mngmnt.get_preorder(call.message.chat.id)):
            message = preorder_pages_generator.create_preorder_posted_page()
            bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                                  reply_markup=message['markup'], parse_mode='HTML')
        else:
            bot.answer_callback_query(call.id, text="Что-то пошло не так. Попробуйте, пожалуйста, снова.")
            get_main_menu(call.message)
    except AttributeError as err:
        attribute_error_handler(err, call)
    except KeyError as err:
        key_error_handler(err, call)


#  Изменить телефонный номер в процессе оформления заказа
@bot.callback_query_handler(func=lambda call: call.data == 'change-phone-number')
def change_phone_number(call):
    message = preorder_pages_generator.create_change_phone_number_page()
    bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                          reply_markup=message['markup'], parse_mode='HTML')


#  Изменить дату предзаказа
@bot.callback_query_handler(func=lambda call: call.data == 'change-preorder-date')
def change_preorder_date(call):
    try:
        chat_id = call.message.chat.id
        if preorder_mngmnt.get_preorder(chat_id).get_item_list():
            message = preorder_pages_generator.create_warning_change_date_page()
            bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                                  reply_markup=message['markup'], parse_mode='HTML')
        else:
            change_preorder_date_approved(call)
    except AttributeError as err:
        attribute_error_handler(err, call)
    except KeyError as err:
        key_error_handler(err, call)


#  Изменение даты заказа было подтверждено
@bot.callback_query_handler(func=lambda call: call.data == 'change_preorder_date_approved')
def change_preorder_date_approved(call):
    try:
        chat_id = call.message.chat.id
        preorder_mngmnt.remove_preorder(chat_id)
        call_data = 'main_menu_hire_' + customer_mngmnt.get_customer(chat_id).get_current_type_of_thing()
        call.data = call_data
        get_calendar(call)
    except AttributeError as err:
        attribute_error_handler(err, call)
    except KeyError as err:
        key_error_handler(err, call)


#bot.polling(none_stop=True, interval=0)
while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception:
        time.sleep(15)
        continue
