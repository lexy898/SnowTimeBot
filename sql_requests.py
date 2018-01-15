import sqlite3
import logging
from datetime import datetime

import os

import sys

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')
_DB_PATH = "hire.db3"


# Получить аксессуары по типу
def get_things_by_type(type_of_thing):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ACCESSORIES WHERE TYPE = \"" + str(type_of_thing) + "\"")
        things = cursor.fetchall()
        conn.close()
        return things
    except sqlite3.DatabaseError as err:
        logging.error(u'Method:'+sys._getframe().f_code.co_name+' sqlite3.DatabaseError: ' + str(err) + '')


#  Получить ссылку на изображение по ID
def get_url_by_item(item):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT PICTURE_URL FROM ACCESSORIES WHERE ID = \"" + str(item) + "\"")
        url = cursor.fetchone()[0]
        conn.close()
        return url
    except sqlite3.DatabaseError as err:
        logging.error(u'Method:'+sys._getframe().f_code.co_name+' sqlite3.DatabaseError: ' + str(err) + '')


# Получить аксессуар по ID
def get_thing_by_ID(thing_id):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ACCESSORIES WHERE ID = \"" + str(thing_id) + "\"")
        thing = cursor.fetchone()
        conn.close()
        return thing
    except sqlite3.DatabaseError as err:
        logging.error(u'Method:'+sys._getframe().f_code.co_name+' sqlite3.DatabaseError: ' + str(err) + '')


#  Загрузить всех клиентов
def get_all_customers():
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CUSTOMERS")
        customers = cursor.fetchall()
        conn.close()
        customers_dict = {}
        for customer in customers:
            customer_info = {"NAME": customer[1], "PHONE": customer[2]}
            customers_dict[str(customer[0])] = customer_info
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
        print('хуйхуй')
        cursor.execute("INSERT INTO CUSTOMERS (\'CHAT_ID\', \'JOIN_DATE\') VALUES (\'" + str(chat_id)
                       + "\', \'" + datetime.strftime(now, "%Y-%m-%d %H:%M:%S") + "\')")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'Method:' + sys._getframe().f_code.co_name + ' sqlite3.DatabaseError: ' + str(err) + '')


#  Добавить имя клиента
def add_customer_name(chat_id, name):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        print('хуйхуй2')
        cursor.execute("UPDATE CUSTOMERS SET NAME = \'" + name + "\' WHERE CHAT_ID = \'" + str(chat_id) + "\'")
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
