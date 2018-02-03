from datetime import datetime
import sql_requests
import logging
import sys

from customer import customer


class CustomerManagement:

    _customers = {}  # словарь, содержащий всех клиентов {chat_id: customer}

    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR,
                            filename=u'log.txt')
    #{'CHAT_ID': 158041048, 'USERNAME': 'Akozitsin', 'NAME': 'Alexey', 'LAST_NAME': 'Kozitsin', 'PHONE': '79886667788', 'JOIN_DATE': '2018-01-23 21:39:53'}

    @classmethod
    def init_customers(cls):
        db_customers = sql_requests.get_all_customers()
        try:
            for db_customer in db_customers:
                new_customer = customer.Customer()
                new_customer.set_chat_id(db_customer['CHAT_ID'])
                new_customer.set_username(db_customer['USERNAME'])
                new_customer.set_name(db_customer['NAME'])
                new_customer.set_last_name(db_customer['LAST_NAME'])
                new_customer.set_phone(db_customer['PHONE'])
                new_customer.set_join_date(db_customer['JOIN_DATE'])
                cls._customers[db_customer['CHAT_ID']] = new_customer
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')

    @classmethod
    def check_existence_client(cls, chat_id):
        if cls.get_customer(chat_id) is not None:
            return True
        else:
            return False

    @classmethod
    def get_customer(cls, chat_id):
        try:
            return cls._customers[chat_id]
        except KeyError:
            return None

    @classmethod
    def add_new_customer(cls, message):
        chat_id = message.chat.id
        now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        new_customer = customer.Customer()
        new_customer.set_chat_id(chat_id)
        new_customer.set_username(message.chat.username)
        new_customer.set_name(message.chat.first_name)
        new_customer.set_last_name(message.chat.last_name)
        new_customer.set_join_date(now)
        cls._customers[chat_id] = new_customer
        sql_requests.add_new_customer(new_customer)

    @classmethod
    def update_customer_phone(cls, chat_id, phone):
        customer = cls.get_customer(chat_id)
        customer.set_phone(phone)
        sql_requests.update_customer_phone(chat_id, phone)


    # def add_customer(self, chat_id):
    #     self._customers[chat_id] = {}
    #     sql_requests.add_new_customer(chat_id)
    #
    #
    #
    # def get_customer_phone(self, chat_id):
    #     try:
    #         customer_info = self._customers[chat_id]
    #         return customer_info['PHONE']
    #     except KeyError as err:
    #         return None
    #
    # def add_customer_info(self, message):
    #     chat_id = message.chat.id
    #     self._customers[chat_id].update({'CHAT_ID': message.chat.id,
    #                                      'NAME': message.chat.first_name,
    #                                      'LAST_NAME': message.chat.last_name,
    #                                      'USERNAME': message.chat.username})
    #     sql_requests.add_customer_info(chat_id, self._customers[chat_id])
    #
    # def update_customer_phone(self, chat_id, phone):
    #     try:
    #         customer_info = self._customers[chat_id]
    #         customer_info['PHONE'] = phone
    #         self._customers[chat_id] = customer_info
    #
    #         sql_requests.update_customer_phone(chat_id, phone)
    #     except KeyError as err:
    #         logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
    #
    # def get_customer_info(self, chat_id):
    #     try:
    #         return self._customers[chat_id]
    #     except KeyError as err:
    #         logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
    #         return {}
    #
    # def set_current_calendar_month(self, chat_id, date):
    #     self._current_calendar_month[chat_id] = date
    #
    # def get_current_calendar_month(self, chat_id):
    #     try:
    #         return self._current_calendar_month[chat_id]
    #     except KeyError as err:
    #         logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
    #         return None
    #
    # def set_current_type_of_thing(self, chat_id, type_of_thing):
    #     self._current_type_of_thing[chat_id] = type_of_thing
    #
    # def get_current_type_of_thing(self, chat_id):
    #     try:
    #         return self._current_type_of_thing[chat_id]
    #     except KeyError as err:
    #         logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
    #         return None
    #
    # def set_current_page(self, chat_id, current_page):
    #     self._current_page[chat_id] = current_page
    #
    # def get_current_page(self, chat_id):
    #     try:
    #         return self._current_page[chat_id]
    #     except KeyError as err:
    #         logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
    #         return 0
