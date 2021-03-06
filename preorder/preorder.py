import logging
import sys


class Preorder:
    def __init__(self):
        self._chat_id = None
        self._item_list = []
        self._start_date = None
        self._days = 1
        self._price = None
        self._actual_price = None
        self._discount = None
        self._phone = None

        logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR,
                            filename=u'log.txt')

    # Setters block
    def set_chat_id(self, chat_id):
        self._chat_id = chat_id

    def set_item_list(self, item_list):
        self._item_list = list(item_list)

    def set_start_date(self, start_date):
        self._start_date = start_date

    def set_days(self, days):
        self._days = days

    def set_price(self, price):
        self._price = price

    def set_actual_price(self, actual_price):
        self._actual_price = actual_price

    def set_discount(self, discount):
        self._discount = discount

    def set_phone(self, phone):
        self._phone = phone

    # Getters block
    def get_chat_id(self):
        return self._chat_id

    def get_item_list(self):
        return self._item_list

    def get_start_date(self):
        return self._start_date

    def get_days(self):
        return self._days

    def get_price(self):
        return self._price

    def get_actual_price(self):
        return self._actual_price

    def get_discount(self):
        return self._discount

    def get_phone(self):
        return self._phone

    # Other block
    def add_item(self, item_id):
        self._item_list.append(item_id)

    def remove_item(self, item_id):
        try:
            self._item_list.remove(item_id)
        except ValueError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' ValueError: ' + str(err) + '')


