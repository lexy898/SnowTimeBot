import sqlite3
import logging
from datetime import datetime

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
    try:
        conn = sqlite3.connect(_DB_PATH)
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CUSTOMERS")
        customers = cursor.fetchall()
        conn.close()
        customers_dict = {}
        for customer in customers:
            customers_dict[str(customer['CHAT_ID'])] = customer
        conn.close()
        return customers_dict
    except sqlite3.DatabaseError as err:
        logging.error(u'Method:' + sys._getframe().f_code.co_name + ' sqlite3.DatabaseError: ' + str(err) + '')


#  добавить нового клиента
def add_new_customer(chat_id):
    now = datetime.now()
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO CUSTOMERS (\'CHAT_ID\', \'JOIN_DATE\') VALUES (\'" + str(chat_id)
                       + "\', \'" + datetime.strftime(now, "%Y-%m-%d %H:%M:%S") + "\')")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'Method:' + sys._getframe().f_code.co_name + ' sqlite3.DatabaseError: ' + str(err) + '')


#  Добавить инфу по клиенту
def add_customer_info(chat_id, customer_info):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE CUSTOMERS "
                       "SET NAME = \'" + str(customer_info['NAME']) + "\', "
                       "LAST_NAME = \'" + str(customer_info['LAST_NAME']) + "\', "
                       "USERNAME = \'" + str(customer_info['USERNAME']) + "\' "
                       "WHERE CHAT_ID = \'" + str(chat_id) + "\'")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'Method:' + sys._getframe().f_code.co_name + ' sqlite3.DatabaseError: ' + str(err) + '')


#  Обновить номер телефона клиента
def update_customer_phone(chat_id, phone):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE CUSTOMERS "
                       "SET PHONE = \'" + str(phone) + "\' WHERE CHAT_ID = \'" + str(chat_id) + "\'")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'Method:' + sys._getframe().f_code.co_name + ' sqlite3.DatabaseError: ' + str(err) + '')
'''
# Сохранить вещи в БД
def save_things(results, company):
    default = "-"
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM COMPANY WHERE company_name ='" + str(company) + "'")
        company = cursor.fetchone()[0]
        for i in range(len(results)):
            thing = results[i]
            cursor.execute("INSERT INTO result VALUES (\""
                           + str(thing["defaultCode_string"]) + "\","
                           + str(thing["productWhitePrice_rub_double"]) + ","
                           + str(thing["actualPrice_rub_double"]) + ",\""
                           + str(thing["name_text_ru"]).replace('"', '') + "\",\""
                           + str(thing.get("sizes_ru_string_mv", default)) + "\", \""
                           + str(company) + ","
                           + datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S") + "\")")
            conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        print("Error: ", err)


# Добавить новые вещи в БД
def add_new_things(new_things, company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM COMPANY WHERE company_name ='" + str(company) + "'")
        company = cursor.fetchone()[0]
        for thing in new_things:
            print("INSERT INTO result VALUES (\""
                  + str(thing[0]) + "\","
                  + str(thing[1]) + ","
                  + str(thing[2]) + ",\""
                  + str(thing[3]).replace('"', '') + "\",\""
                  + str(thing[4]) + "\","
                  + str(company) + ",\""
                  + datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S") + "\")")
            cursor.execute("INSERT INTO result VALUES (\""
                           + str(thing[0]) + "\","
                           + str(thing[1]) + ","
                           + str(thing[2]) + ",\""
                           + str(thing[3]).replace('"', '') + "\",\""
                           + str(thing[4]) + "\","
                           + str(company) + ",\""
                           + datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S") + "\")")
            conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        print("Error: ", err)


# Удалить вещь по ID
def delete_thing_by_id(id):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM result WHERE defaultCode_string = \"" + str(id) + "\"")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        print("Error: ", err)


# Получить коды вещей указанной компании
def get_things(company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT defaultCode_string FROM result WHERE COMPANY = "
                       "(SELECT id FROM COMPANY WHERE company_name ='" + str(company) + "')")
        things = cursor.fetchall()
        result = [x[0] for x in things]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')
'''
