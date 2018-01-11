from telebot import types


def create_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.row(types.InlineKeyboardButton("Посмотреть доски", callback_data="main_menu_hire_board"))
    markup.row(types.InlineKeyboardButton("Посмотреть ботинки", callback_data="main_menu_hire_boots"))
    markup.row(types.InlineKeyboardButton("Посмотреть маски", callback_data="main_menu_hire_mask"))
    markup.row(types.InlineKeyboardButton("О нас", callback_data="about_us"))
    return markup
