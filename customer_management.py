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

    def check_existence_phone(self, chat_id):
        customer_info = self._customers[chat_id]
        if customer_info['PHONE'] is not None:
            return True
        else:
            return False

    def add_customer_name(self, chat_id, name):
        self._customers[chat_id].update({'NAME': name})
        sql_requests.add_customer_name(chat_id, name)
