import logging
import sys
import sql_requests


class Administrator:
    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR,
                        filename=u'log.txt')
    admin_dict = {}

    @classmethod
    def init_admins(cls):
        admins_db = sql_requests.get_all_admins()
        for admin_db in admins_db:
            admin = Admin(admin_db)
            cls.admin_dict[admin.admin_id] = admin

    @classmethod
    def get_admin(cls, chat_id):
        try:
            return cls.admin_dict[chat_id]
        except KeyError:
            return None


class Admin:

    def __init__(self, admin_db):
        try:
            self.admin_id = admin_db['CHAT_ID']
            self.admin_name = admin_db['NAME']
            self.admin_phone = admin_db['PHONE']
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
