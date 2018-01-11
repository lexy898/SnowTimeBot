import datetime
import telebot
import logging
import config
import main_menu
from telegramcalendar import create_calendar
import pagination
from telebot import types
# import sql_requests
import time

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')

TOKEN = config.get_token()

bot = telebot.TeleBot(TOKEN)

current_shown_dates = {}  # Текущая дата, закрепленная за пользователем
current_type_of_thing = {}  # Текущий тип вещи, закрепленный за пользователем
current_page = {}  # Текущая страница, закрепленная за пользователем


# Создание главного меню
@bot.message_handler(commands=['menu'])
def get_main_menu(message):
    markup = main_menu.create_main_menu()
    bot.send_message(message.chat.id, "ВЫБИРАЙ", reply_markup=markup)


#  Переход на главное меню
@bot.callback_query_handler(func=lambda call: call.data == 'back-to-main-menu')
def get_main_menu_from_outside(call):
    markup = main_menu.create_main_menu()
    bot.edit_message_text("ВЫБИРАЙ", call.from_user.id, call.message.message_id, reply_markup=markup)


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
        logging.error(u'' + str(err) + '')
        get_main_menu_from_outside(call)
        return 0


bot.polling(none_stop=True, interval=0)
