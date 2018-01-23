from datetime import datetime
import logging
import sys

import sql_requests


class OrderManagement:
    def __init__(self):
        self._preorders_list = {}  # Список предзаказов пользователей(корзины) вида:
        # {158041048: {'CHAT_ID': 158041048, 'ITEM_LIST': ['2', '3', '5'], 'START_DATE': '2018-01-19', 'DAYS': '1'}}
        logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR,
                            filename=u'log.txt')

    def create_preorder(self, chat_id, date):
        self._preorders_list[chat_id] = {'CHAT_ID': chat_id, 'ITEM_LIST': [], 'START_DATE': date, 'DAYS': '1'}

    def get_preorder(self, chat_id):
        try:
            return self._preorders_list[chat_id]
        except KeyError as err:
            return {}

    def set_preorder(self, chat_id, preorder):
        try:
            self._preorders_list[chat_id] = preorder
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')

    def get_item_list(self, chat_id):
        try:
            preorder = self._preorders_list[chat_id]
            return preorder['ITEM_LIST']
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
            return []

    def add_item(self, chat_id, item_number):
        try:
            preorder_info = self.get_preorder(chat_id)
            preorder_info['ITEM_LIST'].append(item_number)
            self.set_preorder(chat_id, preorder_info)
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')

    def remove_item(self, chat_id, item_number):
        try:
            preorder_info = self.get_preorder(chat_id)
            preorder_info['ITEM_LIST'].remove(item_number)
            self.set_preorder(chat_id, preorder_info)
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')

    def remove_preorder(self, chat_id):
        try:
            del self._preorders_list[chat_id]
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')

    def create_order(self, customer_info):
        item_list = self.get_item_list(customer_info['CHAT_ID'])
        if item_list:
            sql_requests.create_order(customer_info, self.get_preorder(customer_info['CHAT_ID']))
            return True
        else:
            return False

    def is_preorder_exist(self, chat_id):
        if self.get_preorder(chat_id):
            return True
        else:
            return False

    def get_preorder_date(self, chat_id):
        try:
            preorder = self.get_preorder(chat_id)
            start_date = datetime.strptime(preorder['START_DATE'], "%Y-%m-%d %H:%M:%S")  # Конвертация в формат dateTime
            start_date = datetime.strftime(start_date, "%d-%m-%Y")  # конвертация в str форматированной даты
            return start_date
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
            return None