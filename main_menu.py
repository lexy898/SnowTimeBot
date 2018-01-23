from telebot import types


def create_main_menu(preorder):
    message_text = 'ВЫБИРАЙ'
    markup = types.InlineKeyboardMarkup()
    if preorder:
        item_list = preorder['ITEM_LIST']
        if item_list:
            #  callback_data отсылает к страничке предзаказа
            markup.row(types.InlineKeyboardButton('Мой заказ('+str(len(item_list))+')',
                                                  callback_data='go-to-preorder'))
    markup.row(types.InlineKeyboardButton("Посмотреть доски", callback_data="main_menu_hire_board"))
    markup.row(types.InlineKeyboardButton("Посмотреть ботинки", callback_data="main_menu_hire_boots"))
    markup.row(types.InlineKeyboardButton("Посмотреть маски", callback_data="main_menu_hire_mask"))
    markup.row(types.InlineKeyboardButton("О нас", callback_data="about_us"))
    message = {'message_text': message_text, 'markup': markup}
    return message


