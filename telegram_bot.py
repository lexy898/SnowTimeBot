import datetime
import sys
import telebot
import logging
import config
import main_menu
import order_management
import preorder_pages_generator
from telegramcalendar import create_calendar
import pagination
import customer_management
import input_validator

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')

TOKEN = config.get_token()

bot = telebot.TeleBot(TOKEN)

order_mngmnt = order_management.OrderManagement()  # Управление предзаказами
customer_mngmnt = customer_management.CustomerManagement()  # управление клиентами
input_validate = input_validator.InputValidator()


# Создание главного меню
@bot.message_handler(commands=['start'])
def get_main_menu(message):
    chat_id = message.chat.id
    if not customer_mngmnt.check_existence_client(chat_id):
        customer_mngmnt.add_customer_info(message)
    preorder = order_mngmnt.get_preorder(chat_id)
    message_to_send = main_menu.create_main_menu(preorder)
    bot.send_sticker(chat_id, 'CAADAgADAgAD2INrCdsC2_uAN23lAg')
    bot.send_message(chat_id, message_to_send['message_text'], reply_markup=message_to_send['markup'])
    input_validate.off_input_phone_mode(chat_id)  # Отключаем режим ввода телефона


#  Переход на главное меню
@bot.callback_query_handler(func=lambda call: call.data == 'back-to-main-menu')
def get_main_menu_from_outside(call):
    chat_id = call.message.chat.id
    preorder = order_mngmnt.get_preorder(chat_id)
    message = main_menu.create_main_menu(preorder)
    bot.send_sticker(chat_id, 'CAADAgADAgAD2INrCdsC2_uAN23lAg')
    bot.send_message(chat_id, message['message_text'], reply_markup=message['markup'])
    input_validate.off_input_phone_mode(str(chat_id))  # Отключаем режим ввода телефона


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
            item_number = message.text[22:]
            order_mngmnt.remove_item(chat_id, item_number)
            message_to_send.update(preorder_pages_generator.create_edit_preorder_page(order_mngmnt.get_item_list(chat_id)))
        elif input_validate.check_input_phone_mode(chat_id):
            if input_validate.validation_phone(message.text):
                message_to_send.update(preorder_pages_generator.create_preorder_posted_page())
                customer_mngmnt.update_customer_phone(chat_id, message.text)
                order_mngmnt.create_order(customer_mngmnt.get_customer_info(chat_id))
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
    chat_id = call.message.chat.id
    customer_mngmnt.set_current_type_of_thing(chat_id, call.data[15:].upper())
    if not order_mngmnt.is_preorder_exist(chat_id):
        now = datetime.datetime.now()  # Current date
        date = (now.year, now.month)
        customer_mngmnt.set_current_calendar_month(chat_id, date) # Saving the current date in a dict
        markup = create_calendar(now.year, now.month)
        bot.edit_message_text("Пожалуйста, выберите дату, на которую планируете взять прокат", call.from_user.id,
                              call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        message = pagination.create_list(customer_mngmnt.get_current_type_of_thing(chat_id), 0,
                                         order_mngmnt.get_preorder_date(chat_id))
        bot.edit_message_text(message['message_text'], call.from_user.id,
                              call.message.message_id, reply_markup=message['markup'], parse_mode='HTML')
        bot.answer_callback_query(call.id, text="")


@bot.callback_query_handler(func=lambda call: call.data[0:13] == 'calendar-day-')
def get_day(call):
    chat_id = call.message.chat.id
    saved_date = customer_mngmnt.get_current_calendar_month(chat_id)
    customer_mngmnt.set_current_page(chat_id, 0)
    if saved_date is not None:
        day = call.data[13:]
        date = str(datetime.datetime(int(saved_date[0]), int(saved_date[1]), int(day), 0, 0, 0))
        order_mngmnt.create_preorder(chat_id, date)
        message = pagination.create_list(customer_mngmnt.get_current_type_of_thing(chat_id), 0,
                                         order_mngmnt.get_preorder_date(chat_id))
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
    saved_date = customer_mngmnt.get_current_calendar_month(chat_id)
    if saved_date is not None:
        year, month = saved_date
        month += 1
        if month > 12:
            month = 1
            year += 1
        date = (year, month)
        customer_mngmnt.set_current_calendar_month(chat_id, date)
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
    saved_date = customer_mngmnt.get_current_calendar_month(chat_id)
    if saved_date is not None:
        year, month = saved_date
        month -= 1
        if month < 1:
            month = 12
            year -= 1
        date = (year, month)
        customer_mngmnt.set_current_calendar_month(chat_id, date)
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
    customer_mngmnt.set_current_page(call.message.chat.id, turn_page(call))


@bot.callback_query_handler(func=lambda call: call.data == 'previous-page')
def previous_page(call):
    customer_mngmnt.set_current_page(call.message.chat.id, turn_page(call))


@bot.callback_query_handler(func=lambda call: call.data == 'back-to-pagination')
def previous_page_from_item_page(call):
    chat_id = call.message.chat.id
    try:
        message = pagination.create_list(customer_mngmnt.get_current_type_of_thing(chat_id),
                                         customer_mngmnt.get_current_page(chat_id), order_mngmnt.get_preorder_date(chat_id))
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
            customer_mngmnt.set_current_page(chat_id, customer_mngmnt.get_current_page(chat_id) + 1)
        else:
            customer_mngmnt.set_current_page(chat_id, customer_mngmnt.get_current_page(chat_id) - 1)
        message = pagination.create_list(customer_mngmnt.get_current_type_of_thing(chat_id),
                                         customer_mngmnt.get_current_page(chat_id), order_mngmnt.get_preorder_date(chat_id))
        bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                              reply_markup=message['markup'], parse_mode='HTML')
        bot.answer_callback_query(call.id, text="")
        return customer_mngmnt.get_current_page(chat_id)
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
    order_mngmnt.add_item(chat_id, item_number)
    message = preorder_pages_generator.create_preorder_page(order_mngmnt.get_preorder(chat_id))
    bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                          reply_markup=message['markup'], parse_mode='HTML')
    bot.answer_callback_query(call.id, text="Добавлено")


#  Открыть страничку пагинации с выбором инвентаря
@bot.callback_query_handler(func=lambda call: call.data == 'go-to-pagination')
def go_to_pagination(call):
    previous_page_from_item_page(call)


#  Сохранить предзаказ(создание заказа)
@bot.callback_query_handler(func=lambda call: call.data == 'save-preorder')
def save_preorder(call):
    chat_id = call.message.chat.id
    input_validate.set_input_phone_mode(chat_id)  # Включаем режим ввода телефона
    message = preorder_pages_generator.create_ask_phone_page(customer_mngmnt.get_customer_phone(chat_id))
    bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                          reply_markup=message['markup'], parse_mode='HTML')
    bot.answer_callback_query(call.id, text="")


# Редактировать предзаказ
@bot.callback_query_handler(func=lambda call: call.data == 'edit-preorder')
def edit_preorder(call):
    try:
        chat_id = call.message.chat.id
        message = preorder_pages_generator.create_edit_preorder_page(order_mngmnt.get_item_list(chat_id))
        bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                              reply_markup=message['markup'], parse_mode='HTML')
        bot.answer_callback_query(call.id, text="")
    except KeyError as err:
        bot.answer_callback_query(call.id, text="Что-то пошло не так. Попробуйте, пожалуйста, снова.")
        get_main_menu(call.message)
        logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')


#  Удалить предзаказ. Появляется страничка подтверждения
@bot.callback_query_handler(func=lambda call: call.data == 'delete-preorder')
def delete_preorder(call):
    try:
        chat_id = call.message.chat.id
        message = preorder_pages_generator.create_delete_approve_page(order_mngmnt.get_item_list(chat_id))
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
        order_mngmnt.remove_preorder(chat_id)
        get_main_menu(call.message)
        bot.answer_callback_query(call.id, text="Заказ успешно удален")
    except KeyError as err:
        bot.answer_callback_query(call.id, text="Что-то пошло не так. Попробуйте, пожалуйста, снова.")
        get_main_menu(call.message)
        logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')


#  Отмена удаления предзаказа
@bot.callback_query_handler(func=lambda call: call.data == 'go-to-preorder')
def go_to_preorder(call):
    try:
        chat_id = call.message.chat.id
        message = preorder_pages_generator.create_preorder_page(order_mngmnt.get_preorder(chat_id))
        bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                              reply_markup=message['markup'], parse_mode='HTML')
        bot.answer_callback_query(call.id, text="")
        input_validate.off_input_phone_mode(chat_id)  # Отключаем режим ввода телефона
    except KeyError as err:
        bot.answer_callback_query(call.id, text="Что-то пошло не так. Попробуйте, пожалуйста, снова.")
        get_main_menu(call.message)
        logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')


#  Телефон изменять не нужно
@bot.callback_query_handler(func=lambda call: call.data == 'phone-approved')
def phone_approved(call):
    if order_mngmnt.create_order(customer_mngmnt.get_customer_info(call.message.chat.id)):
        message = preorder_pages_generator.create_preorder_posted_page()
        bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                              reply_markup=message['markup'], parse_mode='HTML')
    else:
        bot.answer_callback_query(call.id, text="Что-то пошло не так. Попробуйте, пожалуйста, снова.")
        get_main_menu(call.message)


#  Изменить телефонный номер в процессе оформления заказа
@bot.callback_query_handler(func=lambda call: call.data == 'change-phone-number')
def change_phone_number(call):
    message = preorder_pages_generator.create_change_phone_number_page()
    bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                          reply_markup=message['markup'], parse_mode='HTML')


#  Изменить дату предзаказа
@bot.callback_query_handler(func=lambda call: call.data == 'change-preorder-date')
def change_preorder_date(call):
    chat_id = call.message.chat.id
    if order_mngmnt.is_preorder_exist(chat_id):
        if order_mngmnt.get_item_list(chat_id):
            message = preorder_pages_generator.create_warning_change_date_page()
            bot.edit_message_text(message['message_text'], call.from_user.id, call.message.message_id,
                                  reply_markup=message['markup'], parse_mode='HTML')
        else:
            change_preorder_date(call)
    else:
        bot.answer_callback_query(call.id, text="Что-то пошло не так. Попробуйте, пожалуйста, снова.")
        get_main_menu(call.message)


#  Изменение даты заказа было подтверждено
@bot.callback_query_handler(func=lambda call: call.data == 'change_preorder_date_approved')
def change_preorder_date(call):
    chat_id = call.message.chat.id
    order_mngmnt.remove_preorder(chat_id)
    call_data = 'main_menu_hire_' + customer_mngmnt.get_current_type_of_thing(chat_id)
    call.data = call_data
    get_calendar(call)


bot.polling(none_stop=True, interval=0)
# while True:
#     try:
#         bot.polling(none_stop=True, interval=0)
#     except Exception:
#         time.sleep(15)
#         continue
