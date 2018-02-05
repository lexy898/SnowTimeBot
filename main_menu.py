from telebot import types
import sql_requests


def create_main_menu(preorder):
    types_of_things = sql_requests.get_all_types_of_things()
    message_text = 'Можешь выбрать все, что тебе нужно: '
    markup = types.InlineKeyboardMarkup()
    if preorder:
        item_list = preorder.get_item_list()
        if item_list:
            #  callback_data отсылает к страничке предзаказа
            markup.row(types.InlineKeyboardButton('Корзина('+str(len(item_list))+')',
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

def about_us_page():
    message_text = "<b>Прокат Сноубордов и аксессуаров в городе Вологда.</b> \n " \
                   "Для наших любимых клиентов мы заранее позаботились о наличии всех размеров ботинок и досок. \n" \
                   "Никто не будет обделен.😉\n" \
                   "<b>Благовещенская 69</b>.\n" \
                   "Круглосуточно на связи <b>+7(911) 504-34-01</b>\n\n" \
                   "Всем белого и пушистого!⛷🏂 "
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("Вернуться на главное меню", callback_data="back-to-main-menu"))
    message = {'message_text': message_text, 'markup': markup}
    return message