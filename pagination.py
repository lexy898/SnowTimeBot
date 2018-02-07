from datetime import datetime
import accessory
from telebot import types
from math import ceil
import sql_requests

ELEMENTS_ON_PAGE = 3


def create_list(customer, page, preorder):
    row = []
    type_of_thing = customer.get_current_type_of_thing()
    date = preorder.get_start_date()
    accessory_list = []
    things = sql_requests.get_things_by_type(type_of_thing)
    for thing in things:
        one_of_accessory = accessory.Accessory(thing)
        if one_of_accessory.accessory_availability(date) and str(one_of_accessory.id) not in preorder.get_item_list():
            accessory_list.append(accessory.Accessory(thing))

    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    date = datetime.strftime(date, "%d-%m-%Y")

    page_count = ceil(len(accessory_list) / ELEMENTS_ON_PAGE)
    if page >= page_count:
        page = page_count - 1
        customer.set_current_page(page)
    limit = len(accessory_list)

    markup = types.InlineKeyboardMarkup()
    position = page * ELEMENTS_ON_PAGE
    if not accessory_list:
        message_text = '📆На дату <b>' + date + '</b> нет выбранного инвентаря 😧\n'
    else:
        message_text = '📆На дату <b>' + date + '</b> есть такой инвентарь:\n\n'
        for i in range(ELEMENTS_ON_PAGE):
            if position < limit:
                try:
                    thing = accessory_list[position]
                except IndexError:
                    position = 0
                    thing = accessory_list[position]
                    page = 0
                if thing.name is not None:
                    message_text += '<b>🚩' + thing.name.upper() + '</b>\n'
                if thing.size is not None:
                    message_text += 'Размер: ' + thing.size + '\n'
                if thing.growth is not None:
                    message_text += 'Подходит для роста: ' + thing.growth + '\n'
                if thing.picture_url is not None:
                    message_text += 'Посмотреть: /item_' + str(thing.id) + '\n\n'
                position += 1
        if page == 0:
            if page_count != 1:
                row = [types.InlineKeyboardButton("➡", callback_data="next-page")]
        else:
            if page + 1 == page_count:
                row = [types.InlineKeyboardButton("⬅", callback_data="previous-page")]
            else:
                row = [types.InlineKeyboardButton("⬅", callback_data="previous-page"),
                       types.InlineKeyboardButton("➡", callback_data="next-page")]

        markup.row(*row)
    row = [types.InlineKeyboardButton("Изменить дату", callback_data="change-preorder-date")]
    markup.row(*row)
    row = [types.InlineKeyboardButton("Вернуться на главное меню", callback_data="back-to-main-menu")]
    markup.row(*row)
    message = {'message_text': message_text, 'markup': markup}
    return message


#  create_list("BOARD")
