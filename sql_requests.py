import sqlite3
import logging
from datetime import datetime, timedelta
from customer import customer
import config
from order import order

import os

import sys

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')
_DB_PATH = str(os.getcwd())+"/hire.db3"


# фабрика для превращения результата запроса в словарь
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Запрос типа SELECT
def select_query(query):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(
            u'Method:' + sys._getframe().f_code.co_name + ' sqlite3.DatabaseError: ' + str(err) + ' Query: ' + query)


# Запрос типа SELECT (Возврвщает таблицу в виде словаря, где ключ - название поля)
def select_query_factory(query):
    try:
        conn = sqlite3.connect(_DB_PATH)
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(
            u'Method:' + sys._getframe().f_code.co_name + ' sqlite3.DatabaseError: ' + str(err) + ' Query: ' + query)


# Запрос типа UPDATE или INSERT
def update_insert_query(query):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(
            u'Method:' + sys._getframe().f_code.co_name + ' sqlite3.DatabaseError: ' + str(err) + ' Query: ' + query)


# Получить аксессуары по типу
def get_things_by_type(type_of_thing):
    query = "SELECT * FROM ACCESSORIES WHERE TYPE = \"" + str(type_of_thing) + "\""
    return select_query(query)


#  Получить ссылку на изображение по ID
def get_url_by_item(item):
    query = "SELECT PICTURE_URL FROM ACCESSORIES WHERE ID = \"" + str(item) + "\""
    return select_query(query)[0]


# Получить аксессуар по ID
def get_thing_by_ID(thing_id):
    query = "SELECT * FROM ACCESSORIES WHERE ID = \"" + str(thing_id) + "\""
    return select_query(query)[0]


#  Загрузить всех клиентов
def get_all_customers():
    query = 'SELECT * FROM CUSTOMERS'
    customers = select_query_factory(query)
    return customers


#  добавить нового клиента
def add_new_customer(new_customer):
    query = "INSERT INTO CUSTOMERS (\'CHAT_ID\', \'USERNAME\', \'NAME\', \'LAST_NAME\', \'JOIN_DATE\')" \
            " VALUES (\'" + str(new_customer.get_chat_id()) + "\', " \
            "\'" + str(new_customer.get_username()) + "\', " \
            "\'" + str(new_customer.get_name()) + "\', " \
            "\'" + str(new_customer.get_last_name()) + "\', " \
            "\'" + str(new_customer.get_join_date()) + "\')"
    update_insert_query(query)


#  Обновить номер телефона клиента
def update_customer_phone(chat_id, phone):
    query = "UPDATE CUSTOMERS SET PHONE = \'" + str(phone) + "\' WHERE CHAT_ID = \'" + str(chat_id) + "\'"
    update_insert_query(query)


#  Создать заказ
def create_order(new_order):
    chat_id = str(new_order.get_chat_id())
    now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    start_date = datetime.strptime(new_order.get_start_date(), "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strftime(start_date + timedelta(days=new_order.get_days()), "%Y-%m-%d %H:%M:%S")
    order_id = ''  # id заказа
    query = 'INSERT INTO ORDERS (CHAT_ID, CREATED_DATE) VALUES ' \
            '(\'' + chat_id + '\', \'' + now + '\')'
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)  # Создаем заказ в таблице ORDERS
        conn.commit()
        cursor.execute(
            'SELECT ORDER_ID FROM ORDERS WHERE rowid=last_insert_rowid();')  # Получаем ID свежесозданного заказа
        order_id += str(cursor.fetchone()[0])
        item_list = new_order.get_item_list()
        for order_item in item_list:
            query = 'INSERT INTO ORDERS_DETAILS (ORDER_ID, CHAT_ID, ITEM_ID, START_DATE, END_DATE, ' \
                    'PHONE, STATUS) VALUES (\'' + order_id + '\', \'' + chat_id + '\', \'' + str(order_item) + '\', ' \
                                                                                                               '\'' + \
                    new_order.get_start_date() + '\', \'' + end_date + '\', \'' + str(new_order.get_phone()) + '\', \'NEW\')'
            cursor.execute(query)
        conn.commit()
        conn.close()
        return order_id
    except sqlite3.DatabaseError as err:
        logging.error(
            u'Method:' + sys._getframe().f_code.co_name + ' sqlite3.DatabaseError: ' + str(err) + ' Query: ' + query)
        return None


#  Метод возвращает все типы вещей
def get_all_types_of_things():
    query = 'SELECT * FROM TYPES_OF_THINGS'
    types = select_query_factory(query)
    types_dict = {}
    for type in types:
        types_dict[type['TYPE']] = type
    return types_dict


#  Метод возвращает все скидочные комплекты
def get_all_discount_sets():
    query = 'SELECT * FROM DISCOUNT_SETS'
    discount_sets = select_query_factory(query)
    for d_set in discount_sets:
        d_set['ITEMS'] = d_set['ITEMS'].split(',')
    return discount_sets


# Метод возвращает список типов тех вещей, которые ему переданы
def get_type_list_by_items(item_list):
    type_list = []
    for item in item_list:
        query = 'SELECT TYPE FROM ACCESSORIES WHERE ID = ' + str(item)
        type_list.append(select_query(query)[0][0])
    return type_list


#  Загрузить всех администраторов
def get_all_admins():
    query = 'SELECT * FROM ADMINS'
    admins = select_query_factory(query)
    return admins


# Обновить статус заказа
def update_order_status(order_id, admin_id, status):
    query = 'UPDATE ORDERS_DETAILS SET STATUS=\'' + status + '\', ADMIN=\'' + str(admin_id) + '\' WHERE ORDER_ID=' \
                                                                                              '' + str(order_id)
    update_insert_query(query)


#  Получить статус заказа
def get_order_status(order_id):
    query = 'SELECT STATUS FROM ORDERS_DETAILS WHERE ORDER_ID = ' + str(order_id)
    return select_query(query)[0][0]


#  Получить администратора заказа
def get_order_admin(order_id):
    query = 'SELECT ADMIN FROM ORDERS_DETAILS WHERE ORDER_ID = ' + str(order_id)
    admin_id = select_query(query)[0][0]
    if admin_id is not None:
        query = 'SELECT * FROM ADMINS WHERE CHAT_ID = ' + str(admin_id)
        return select_query_factory(query)[0]
    else:
        return None
