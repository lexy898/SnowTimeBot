import sql_requests
import logging
import sys


class CustomerManagement:
    def __init__(self):
        self._customers = sql_requests.get_all_customers()  # словарь, содержащий всех клиентов
        logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR,
                            filename=u'log.txt')
        self._current_type_of_thing = {}  # Текущий тип вещи, закрепленный за пользователем
        self._current_page = {}  # Текущая страница, закрепленная за пользователем
        self._current_calendar_month = {}  # Текущий месяц, выбранный в календаре пользователем

    def add_customer(self, chat_id):
        self._customers[chat_id] = {}
        sql_requests.add_new_customer(chat_id)

    def check_existence_client(self, chat_id):
        if chat_id in self._customers:
            return True
        else:
            self.add_customer(chat_id)
            return False

    def get_customer_phone(self, chat_id):
        try:
            customer_info = self._customers[chat_id]
            return customer_info['PHONE']
        except KeyError as err:
            return None

    def add_customer_info(self, message):
        chat_id = message.chat.id
        self._customers[chat_id].update({'CHAT_ID': message.chat.id,
                                         'NAME': message.chat.first_name,
                                         'LAST_NAME': message.chat.last_name,
                                         'USERNAME': message.chat.username})
        sql_requests.add_customer_info(chat_id, self._customers[chat_id])

    def update_customer_phone(self, chat_id, phone):
        try:
            customer_info = self._customers[chat_id]
            customer_info['PHONE'] = phone
            self._customers[chat_id] = customer_info

            sql_requests.update_customer_phone(chat_id, phone)
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')

    def get_customer_info(self, chat_id):
        try:
            return self._customers[chat_id]
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
            return {}

    def set_current_calendar_month(self, chat_id, date):
        self._current_calendar_month[chat_id] = date

    def get_current_calendar_month(self, chat_id):
        try:
            return self._current_calendar_month[chat_id]
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
            return None

    def set_current_type_of_thing(self, chat_id, type_of_thing):
        self._current_type_of_thing[chat_id] = type_of_thing

    def get_current_type_of_thing(self, chat_id):
        try:
            return self._current_type_of_thing[chat_id]
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
            return None

    def set_current_page(self, chat_id, current_page):
        self._current_page[chat_id] = current_page

    def get_current_page(self, chat_id):
        try:
            return self._current_page[chat_id]
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
            return 0
