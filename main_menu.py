from telebot import types
import sql_requests


def create_main_menu(preorder):
    types_of_things = sql_requests.get_all_types_of_things()
    message_text = 'ВЫБИРАЙ'
    markup = types.InlineKeyboardMarkup()
    if preorder:
        item_list = preorder['ITEM_LIST']
        if item_list:
            #  callback_data отсылает к страничке предзаказа
            markup.row(types.InlineKeyboardButton('Мой заказ('+str(len(item_list))+')',
                                                  callback_data='go-to-preorder'))
    for key in types_of_things:
        type_of_thing = types_of_things[key]
        if type_of_thing['ENABLED'] == 'True':
            text = 'Посмотреть ' + type_of_thing['PLURAL_NAME'].lower()
            callback_data = 'main_menu_hire_' + type_of_thing['TYPE'].lower()
            markup.row(types.InlineKeyboardButton(text, callback_data=callback_data))
    markup.row(types.InlineKeyboardButton("О нас", callback_data="about_us"))
    message = {'message_text': message_text, 'markup': markup}
    return message


