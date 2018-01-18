import logging
import re
import sys

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')


class InputValidator:
    def __init__(self):
        self._input_phone_mode = []  # Cписок, содержащий пользователей, которые в режиме ввода телефона
        self._REG_EXP_PHONE = '^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'

    # Установить режим ввода телефона для chat_id
    def set_input_phone_mode(self, chat_id):
        if not self.check_input_phone_mode(chat_id):
            self._input_phone_mode.append(chat_id)

    # Выключить режим ввода телефона для chat_id
    def off_input_phone_mode(self, chat_id):
        count = self._input_phone_mode.count(chat_id)
        for i in range(count):
            try:
                self._input_phone_mode.remove(chat_id)
            except ValueError as err:
                logging.error(u'Method: ' + sys._getframe().f_code.co_name + ' ValueError: ' + str(err) + '')

    # Проверить включен ли режим ввода телефона для chat_id
    def check_input_phone_mode(self, chat_id):
        if chat_id in self._input_phone_mode:
            return True
        else:
            return False

    #  Валидация введенного номера телефона
    def validation_phone(self, phone):
        if re.match(self._REG_EXP_PHONE, phone) is not None:
            return True
        else:
            return False

