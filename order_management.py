from datetime import datetime
import logging
import sys

import notifier
import sql_requests


class OrderManagement:
    def __init__(self):
        self._preorders_list = {}  # Список предзаказов пользователей(корзины) вида:
        # {158041048: {'CHAT_ID': 158041048, 'ITEM_LIST': ['2', '3', '5'], 'START_DATE': '2018-01-19', 'DAYS': '1'}}

        self._orders_list = {}  # Список заказов пользователей вида:
        # {6456: {'CHAT_ID': 158041048, 'ITEM_LIST': ['2', '3', '5'], 'START_DATE': '2018-01-19', 'DAYS': '1',
        #  'END_DATE': '2018-01-20', 'PHONE': '79992188915}}

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
        try:
            chat_id = customer_info['CHAT_ID']
            item_list = self.get_item_list(chat_id)
            preorder = self.get_preorder(chat_id)
            if item_list:
                order_id = sql_requests.create_order(customer_info, self.get_preorder(chat_id))
                self.add_new_order_to_list(order_id, customer_info, preorder)
                self.remove_preorder(chat_id)
                notifier.send_admin_new_order(self.get_order_by_order_id(order_id))
                return True
            else:
                return False
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
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

    def add_new_order_to_list(self, order_id, customer_info, preorder):
        self._orders_list[order_id] = {
            'CHAT_ID': preorder['CHAT_ID'],
            'ITEM_LIST': preorder['ITEM_LIST'],
            'START_DATE': preorder['START_DATE'],
            'DAYS': preorder['DAYS'],
            'PHONE': customer_info['PHONE'],
            'STATUS': 'NEW'
        }

    def get_order_by_order_id(self, order_id):
        try:
            return self._orders_list[order_id]
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
            return {}