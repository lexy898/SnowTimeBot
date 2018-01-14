from telebot import types


def create_main_menu(items_list):
    message_text = 'ВЫБИРАЙ'
    markup = types.InlineKeyboardMarkup()
    if items_list:
        #  callback_data используется аналогичная кнопке "нет" при отмене удаления предзаказа
        markup.row(types.InlineKeyboardButton('Мой заказ('+str(len(items_list))+')',
                                              callback_data='delete-preorder-no'))
    markup.row(types.InlineKeyboardButton("Посмотреть доски", callback_data="main_menu_hire_board"))
    markup.row(types.InlineKeyboardButton("Посмотреть ботинки", callback_data="main_menu_hire_boots"))
    markup.row(types.InlineKeyboardButton("Посмотреть маски", callback_data="main_menu_hire_mask"))
    markup.row(types.InlineKeyboardButton("О нас", callback_data="about_us"))
    message = {'message_text': message_text, 'markup': markup}
    return message


