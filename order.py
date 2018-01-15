class Order:
    def __init__(self):
        self._chat_id = ''
        self._phone = ''
        self._item_list = ''
        self._start_date = ''

    def set_chat_id(self, chat_id):
        self._chat_id = chat_id

    def set_phone(self, phone):
        self._phone = phone

    def set_item_list(self, item_list):
        self._item_list = item_list

    def set_start_date(self, start_date):
        self._start_date = start_date

    def get_chat_id(self):
        return self._chat_id

    def get_phone(self):
        return self._phone

    def get_item_list(self):
        return self._item_list

    def get_start_date(self):
        return self._start_date
