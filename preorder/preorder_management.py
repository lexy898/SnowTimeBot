from datetime import datetime
import logging
import sys
from preorder import preorder
import notifier
import sql_requests


class PreorderManagement:
    _preorders_list = {}  # Список предзаказов пользователей вида: {158041048: Preorder}

    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR,
                            filename=u'log.txt')

    @classmethod
    def get_preorder(cls, chat_id):
        try:
            return cls._preorders_list[chat_id]
        except KeyError:
            return None

    @classmethod
    def add_new_preorder(cls, new_preorder):
        chat_id = new_preorder.get_chat_id()
        if chat_id is not None:
            cls._preorders_list[chat_id] = new_preorder

    @classmethod
    def remove_preorder(cls, chat_id):
        try:
            del cls._preorders_list[chat_id]
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')

    @classmethod
    def is_preorder_exist(cls, chat_id):
        if cls.get_preorder(chat_id):
            return True
        else:
            return False
