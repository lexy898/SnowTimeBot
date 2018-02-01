from datetime import datetime
import logging
import sys

import notifier
import sql_requests


class OrderManagement:

    _orders_list = {}  # Список заказов пользователей вида {6456: Order}, где 6456 - ID заказа

    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR,
                            filename=u'log.txt')

    # def create_order(self, customer_info):
    #     try:
    #         chat_id = customer_info['CHAT_ID']
    #         item_list = self.get_item_list(chat_id)
    #         preorder = self.get_preorder(chat_id)
    #         if item_list:
    #             order_id = sql_requests.create_order(customer_info, self.get_preorder(chat_id))
    #             self.add_new_order_to_list(order_id, customer_info, preorder)
    #             self.remove_preorder(chat_id)
    #             notifier.send_admin_new_order(self.get_order_by_order_id(order_id))
    #             return True
    #         else:
    #             return False
    #     except KeyError as err:
    #         logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
    #         return False
    #
    #
    # def add_new_order_to_list(self, order_id, customer_info, preorder):
    #     self._orders_list[order_id] = {
    #         'CHAT_ID': preorder['CHAT_ID'],
    #         'ITEM_LIST': preorder['ITEM_LIST'],
    #         'START_DATE': preorder['START_DATE'],
    #         'DAYS': preorder['DAYS'],
    #         'PHONE': customer_info['PHONE'],
    #         'STATUS': 'NEW'
    #     }
    #
    # def get_order_by_order_id(self, order_id):
    #     try:
    #         return self._orders_list[order_id]
    #     except KeyError as err:
    #         logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
    #         return {}