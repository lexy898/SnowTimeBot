import sql_requests
import calendar
from datetime import datetime
import logging
import sys
import math


class PriceManagement:
    def __init__(self):
        self._types = sql_requests.get_all_types_of_things()  # Список словарей вида:
        # 'MASK': {'TYPE': 'MASK', 'DESCRIPTION': 'Маска', 'WEEKDAY_PRICE': 100, 'WEEKEND_PRICE': 100}

        self._discount_sets = sql_requests.get_all_discount_sets()  # Содержит словари вида:
        #  {'SET_ID': 1, 'PRICE': 300, 'IS_WEEKEND': '', 'ITEMS': ['BOOTS', 'BOARD']}

        self._WEEKDAYS = [0, 1, 2, 3, 4]  # Будние дни
        self._WEEKENDS = [5, 6]  # Выходные
        self._WEEKDAY = 'WEEKDAY'  # Будний день
        self._WEEKEND = 'WEEKEND'  # Выходной день

        logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR,
                            filename=u'log.txt')

        # self._CART_1 = 300  # Комплект ботинки доска будни
        # self._CART_2 = 400  # Комплект ботинки доска выходные
        # self._CART_3 = 400  # Комплект ботинки доска маска/шлем будни
        # self._CART_4 = 500  # Комплект ботинки доска маска/шлем выходные
        # self._CART_5 = 500  # Комплект ботинки доска шлем и маска будни
        # self._CART_6 = 600  # Комплект ботинки доска шлем и маска выходные

    def _get_discount_set_by_id(self, set_id):
        try:
            for discount_set in self._discount_sets:
                if discount_set['SET_ID'] == set_id:
                    return discount_set
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
            return {}

    def get_preorder_price_with_discount(self, preorder):
        day_of_week = self._define_day_of_week(preorder)
        discount_sets = self._get_sets_by_day_of_week(day_of_week)
        preorder_item_list = self._get_preorder_item_list(preorder)
        preorder_item_types_list = sql_requests.get_type_list_by_items(preorder_item_list)
        original_preorder_item_types_list = preorder_item_types_list.copy()
        preorder_price = 0
        while True:
            max_discount_set_id = self.get_max_discount_set(discount_sets, preorder_item_types_list, day_of_week)
            if max_discount_set_id is not None:
                preorder_item_types_list = self._remove_set_from_preorder_item_types_list(
                    preorder_item_types_list, self._get_discount_set_by_id(max_discount_set_id))
                preorder_price += self._get_discount_set_by_id(max_discount_set_id)['PRICE']
            else:
                break
        if preorder_item_types_list is not []:
            for preorder_item_type in preorder_item_types_list:
                preorder_price += self._get_price_by_item_type(preorder_item_type, day_of_week)
        full_preorder_price = 0
        for preorder_item_type in original_preorder_item_types_list:
            full_preorder_price += self._get_price_by_item_type(preorder_item_type, day_of_week)
        discount = full_preorder_price - preorder_price
        return {'preorder_price': str(preorder_price), 'full_preorder_price': str(full_preorder_price),
                'discount': str(discount)}


    def _get_price_by_item_type(self, item_type, day_of_week):
        try:
            type_of_thing = self._types[item_type]
            if day_of_week == self._WEEKDAY:
                price = type_of_thing['WEEKDAY_PRICE']
            elif day_of_week == self._WEEKEND:
                price = type_of_thing['WEEKEND_PRICE']
            else:
                price = 0
            return price
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
            return 0

    def _define_day_of_week(self, preorder):
        try:
            start_date = datetime.strptime(preorder.get_start_date(), "%Y-%m-%d %H:%M:%S")
            day_of_week = calendar.weekday(start_date.year, start_date.month, start_date.day)
            if day_of_week in self._WEEKDAYS:
                return self._WEEKDAY
            elif day_of_week in self._WEEKENDS:
                return self._WEEKEND
            else:
                return None
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
            return None

    def _get_sets_by_day_of_week(self, day):
        sets = []
        for d_set in self._discount_sets:
            if day == self._WEEKDAY:
                if d_set['IS_WEEKEND'] != 'True':
                    sets.append(d_set)
            elif day == self._WEEKEND:
                if d_set['IS_WEEKEND'] == 'True':
                    sets.append(d_set)
        return sets

    def _get_preorder_item_list(self, preorder):
        try:
            return preorder.get_item_list()
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
            return []

    def _calculate_discount(self, day_of_week, discount_set):
        is_weekend = True
        price_without_disc = 0
        discount_types_list = discount_set['ITEMS']
        if day_of_week != self._WEEKEND:
            is_weekend = False
        for discount_type in discount_types_list:
            for type_of_thing in self._types:
                if (discount_type == type_of_thing) and is_weekend:
                    price_without_disc += int(self._types[type_of_thing]['WEEKEND_PRICE'])
                    break
                elif (discount_type == type_of_thing) and is_weekend is not True:
                    price_without_disc += int(self._types[type_of_thing]['WEEKDAY_PRICE'])
                    break
        discount = 100 - math.ceil((int(discount_set['PRICE']) / price_without_disc) * 100)
        return discount

    def _remove_set_from_preorder_item_types_list(self, preorder_item_types_list, discount_set):
        try:
            set_items = discount_set['ITEMS']
            for set_item in set_items:
                del preorder_item_types_list[preorder_item_types_list.index(set_item)]
            return preorder_item_types_list
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
            return preorder_item_types_list

    def get_max_discount_set(self, discount_sets, preorder_item_types_list, day_of_week):
        discount = 0
        max_discount_set_id = None
        for discount_set in discount_sets:
            set_items = discount_set['ITEMS']
            if set(set_items).issubset(set(preorder_item_types_list)): # Если сет содержится в предзаказе
                #set_price = discount_set['PRICE']  # получаем сколько стоит сет
                current_set_discount = self._calculate_discount(day_of_week,
                                                                discount_set)  # Высчитываем скидку от текущего сета
                if current_set_discount >= discount:
                    discount = current_set_discount
                    max_discount_set_id = discount_set['SET_ID']
        return max_discount_set_id


# print(calendar.weekday(2018, 1, 25))
