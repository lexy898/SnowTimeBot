from datetime import datetime
import logging
from order import order
from preorder import preorder_management
import sys

import notifier
import sql_requests


class OrderManagement:
    _orders_list = {}  # Список заказов пользователей вида {6456: Order}, где 6456 - ID заказа

    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR,
                        filename=u'log.txt')

    @classmethod
    def create_order(cls, preorder):
        if preorder.get_item_list():
            chat_id = preorder.get_chat_id()

            new_order = order.Order()
            new_order.set_chat_id(chat_id)
            new_order.set_item_list(preorder.get_item_list())
            new_order.set_start_date(preorder.get_start_date())
            new_order.set_days(preorder.get_days())
            new_order.set_price(preorder.get_price())
            new_order.set_actual_price(preorder.get_actual_price())
            new_order.set_discount(preorder.get_discount())
            new_order.set_phone(preorder.get_phone())
            new_order.set_order_id(sql_requests.create_order(new_order))  # Заказ записывается в БД

            cls.add_new_order(new_order)
            preorder_management.PreorderManagement.remove_preorder(chat_id)
            notifier.send_admin_new_order(new_order)
            return True
        else:
            return False

    @classmethod
    def add_new_order(cls, new_order):
        order_id = new_order.get_order_id()
        if order_id is not None:
            cls._orders_list[order_id] = new_order

    @classmethod
    def get_order_by_order_id(cls, order_id):
        try:
            return cls._orders_list[order_id]
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
            return None

