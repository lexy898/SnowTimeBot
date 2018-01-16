import sql_requests


class CustomerManagement:
    def __init__(self):
        self._customers = sql_requests.get_all_customers()  # словарь, содержащий всех клиентов

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
        except KeyError:
            return None

    def add_customer_info(self, message):
        chat_id = str(message.chat.id)
        self._customers[chat_id].update({'NAME':      message.chat.first_name,
                                         'LAST_NAME': message.chat.last_name,
                                         'USERNAME':  message.chat.username})
        sql_requests.add_customer_info(chat_id, self._customers[chat_id])
