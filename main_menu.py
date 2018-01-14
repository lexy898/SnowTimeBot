from telebot import types


def create_main_menu():
    message_text = 'ВЫБИРАЙ'
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("Посмотреть доски", callback_data="main_menu_hire_board"))
    markup.row(types.InlineKeyboardButton("Посмотреть ботинки", callback_data="main_menu_hire_boots"))
    markup.row(types.InlineKeyboardButton("Посмотреть маски", callback_data="main_menu_hire_mask"))
    markup.row(types.InlineKeyboardButton("О нас", callback_data="about_us"))
    message = {'message_text': message_text, 'markup': markup}
    return message

