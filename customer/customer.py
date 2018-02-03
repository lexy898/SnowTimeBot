import logging
import sys


class Customer:
    def __init__(self):
        self._chat_id = None
        self._username = None
        self._name = None
        self._last_name = None
        self._phone = None
        self._join_date = None
        self._current_type_of_thing = None
        self._current_page = None
        self._current_calendar_month = None

    # Setters block
    def set_chat_id(self, chat_id):
        self._chat_id = chat_id

    def set_username(self, username):
        self._username = username

    def set_name(self, name):
        self._name = name

    def set_last_name(self, last_name):
        self._last_name = last_name

    def set_phone(self, phone):
        self._phone = phone

    def set_join_date(self, join_date):
        self._join_date = join_date

    def set_current_type_of_thing(self, current_type_of_thing):
        self._current_type_of_thing = current_type_of_thing

    def set_current_page(self, current_page):
        self._current_page = current_page

    def set_current_calendar_month(self, current_calendar_month):
        self._current_calendar_month = current_calendar_month

    # Getters block
    def get_chat_id(self):
        return self._chat_id

    def get_username(self):
        return self._username

    def get_name(self):
        return self._name

    def get_last_name(self):
        return self._last_name

    def get_phone(self):
        return self._phone

    def get_join_date(self):
        return self._join_date

    def get_current_type_of_thing(self):
        return self._current_type_of_thing

    def get_current_page(self):
        return self._current_page

    def get_current_calendar_month(self):
        return self._current_calendar_month
