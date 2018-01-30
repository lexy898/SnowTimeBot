import sqlite3
import logging
from datetime import datetime, timedelta

import os

import sys

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')
_DB_PATH = "hire.db3"


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
        logging.error(u'Method:'+sys._getframe().f_code.co_name+' sqlite3.DatabaseError: ' + str(err) + ' Query: '+query)


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
        logging.error(u'Method:'+sys._getframe().f_code.co_name+' sqlite3.DatabaseError: ' + str(err) + ' Query: '+query)


# Запрос типа UPDATE или INSERT
def update_insert_query(query):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'Method:' + sys._getframe().f_code.co_name + ' sqlite3.DatabaseError: ' + str(err) + ' Query: ' + query)


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
    customers_dict = {}
    for customer in customers:
        customers_dict[customer['CHAT_ID']] = customer
    return customers_dict


#  добавить нового клиента
def add_new_customer(chat_id):
    now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    query = "INSERT INTO CUSTOMERS (\'CHAT_ID\', \'JOIN_DATE\') VALUES (\'" + str(chat_id) + \
            "\', \'" + now + "\')"
    update_insert_query(query)


#  Добавить инфу по клиенту
def add_customer_info(chat_id, customer_info):
    query = "UPDATE CUSTOMERS SET NAME = \'" + str(customer_info['NAME']) + "\', " \
             "LAST_NAME = \'" + str(customer_info['LAST_NAME']) + "\', " \
             "USERNAME = \'" + str(customer_info['USERNAME']) + "\' " \
             "WHERE CHAT_ID = \'" + str(chat_id) + "\'"
    update_insert_query(query)


#  Обновить номер телефона клиента
def update_customer_phone(chat_id, phone):
    query = "UPDATE CUSTOMERS SET PHONE = \'" + str(phone) + "\' WHERE CHAT_ID = \'" + str(chat_id) + "\'"
    update_insert_query(query)


#  Создать заказ
def create_order(customer_info, order):
    chat_id = str(customer_info['CHAT_ID'])
    now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    start_date = datetime.strptime(order['START_DATE'], "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strftime(start_date + timedelta(days=1), "%Y-%m-%d %H:%M:%S")
    order_id = '' # id заказа
    query = 'INSERT INTO ORDERS (CHAT_ID, CREATED_DATE) VALUES ' \
            '(\'' + chat_id + '\', \'' + now + '\')'
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query) # Создаем заказ в таблице ORDERS
        conn.commit()
        cursor.execute('SELECT ORDER_ID FROM ORDERS WHERE rowid=last_insert_rowid();') # Получаем ID свежесозданного заказа
        order_id += str(cursor.fetchone()[0])
        for order_item in order['ITEM_LIST']:
            query = 'INSERT INTO ORDERS_DETAILS (ORDER_ID, CHAT_ID, ITEM_ID, START_DATE, END_DATE, ' \
                    'PHONE, STATUS) VALUES (\''+ order_id +'\', \''+ chat_id +'\', \''+ str(order_item) +'\', ' \
                    '\'' + order['START_DATE'] + '\', \'' + end_date + '\', \'' + str(customer_info['PHONE']) +'\', \'NEW\')'
            cursor.execute(query)
        conn.commit()
        conn.close()
        return order_id
    except sqlite3.DatabaseError as err:
        logging.error(u'Method:' + sys._getframe().f_code.co_name + ' sqlite3.DatabaseError: ' + str(err) + ' Query: ' + query)
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


print(get_all_discount_sets())