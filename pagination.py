from telebot import types
from math import ceil
import sql_requests

ELEMENTS_ON_PAGE = 3


def create_list(type_of_thing, page):
    accessories = sql_requests.get_things_by_type(type_of_thing)

    page_count = ceil(len(accessories) / ELEMENTS_ON_PAGE)
    limit = len(accessories)

    markup = types.InlineKeyboardMarkup()
    position = page * ELEMENTS_ON_PAGE
    message_text = ''

    for i in range(ELEMENTS_ON_PAGE):
        if position < limit:
            try:
                thing = accessories[position]
            except IndexError:
                position = 0
                thing = accessories[position]
                page = 0
            if thing[1] is not None:
                message_text += '<b>' + thing[1].upper() + '</b>\n'
            if thing[4] is not None:
                message_text += 'Размер: ' + thing[4] + '\n'
            if thing[5] is not None:
                message_text += 'Подходит для роста: ' + thing[5] + '\n'
            if thing[3] is not None:
                message_text += 'Посмотреть: /item_' + str(thing[0]) + '\n\n'
            position += 1
    if message_text == '':
        message_text = 'Инвентарь отсутствует'
        row = [types.InlineKeyboardButton("Вернуться на главное меню", callback_data="back-to-main-menu")]
        markup.row(*row)
    else:
        if page == 0:
            row = [types.InlineKeyboardButton(" ", callback_data="ignore")]
        else:
            row = [types.InlineKeyboardButton("<", callback_data="previous-page")]
        if page + 1 == page_count:
            row.append(types.InlineKeyboardButton(" ", callback_data="ignore"))
        else:
            row.append(types.InlineKeyboardButton(">", callback_data="next-page"))
        markup.row(*row)
        row = [types.InlineKeyboardButton("Вернуться на главное меню", callback_data="back-to-main-menu")]
        markup.row(*row)
    message = {'message_text': message_text, 'markup': markup}
    return message


#  create_list("BOARD")
