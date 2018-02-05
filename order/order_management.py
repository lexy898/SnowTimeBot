import logging
from order import order, order_pages_generator
from preorder import preorder_management
import sys
import administrator
import notifier
import sql_requests


class OrderStatuses:
    def __init__(self):
        self.NEW = 'NEW'
        self.IN_WORK = 'IN_WORK'
        self.APPROVED = 'APPROVED'
        self.CLOSED = 'CLOSED'


class OrderManagement:
    _orders_list = {}  # Список заказов пользователей вида {6456: Order}, где 6456 - ID заказа

    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR,
                        filename=u'log.txt')
    order_statuses = OrderStatuses()

    @classmethod
    def create_order(cls, preorder):
        if preorder.get_item_list():
            chat_id = preorder.get_chat_id()

            new_order = order.Order()
            new_order.set_chat_id(chat_id)
            new_order.set_item_list(preorder.get_item_list())
            new_order.set_start_date(preorder.get_start_date())
            new_order.set_days(preorder.get_days())
            new_order.set_price(preorder.get_price())
            new_order.set_actual_price(preorder.get_actual_price())
            new_order.set_discount(preorder.get_discount())
            new_order.set_phone(preorder.get_phone())
            new_order.set_order_id(sql_requests.create_order(new_order))  # Заказ записывается в БД

            cls.add_new_order(new_order)
            preorder_management.PreorderManagement.remove_preorder(chat_id)
            notifier.send_admin_new_order(new_order)
            return new_order.get_order_id()
        else:
            return None

    @classmethod
    def add_new_order(cls, new_order):
        order_id = new_order.get_order_id()
        if order_id is not None:
            cls._orders_list[order_id] = new_order

    @classmethod
    def get_order_by_order_id(cls, order_id):
        try:
            return cls._orders_list[order_id]
        except KeyError as err:
            logging.error(u'Method:' + sys._getframe().f_code.co_name + ' KeyError: ' + str(err) + '')
            return None

    #  Взять заказ в работу
    @classmethod
    def processing_order(cls, order_id, order_admin):
        global message
        if order_admin is not None:
            order_status = sql_requests.get_order_status(order_id)
            if order_status == cls.order_statuses.NEW:
                sql_requests.update_order_status(order_id, order_admin.admin_id, cls.order_statuses.IN_WORK)
                notifier.send_customer_processing_order(cls.get_order_by_order_id(order_id))
                message = order_pages_generator.admin_create_order_in_processing_page(cls.get_order_by_order_id(order_id))
            else:
                admin = administrator.Admin(sql_requests.get_order_admin(order_id))
                message = order_pages_generator.admin_create_order_unavailable_page(admin, order_id)
        else:
            message = order_pages_generator.admin_create_is_not_admin_page()
        return message

    #  Подтвердить заказ
    @classmethod
    def approve_order(cls, order_id, order_admin):
        global message
        if order_admin is not None:
            order_status = sql_requests.get_order_status(order_id)
            if order_status == cls.order_statuses.IN_WORK:
                sql_requests.update_order_status(order_id, order_admin.admin_id, cls.order_statuses.APPROVED)
                notifier.send_customer_approve_order(cls.get_order_by_order_id(order_id))
                message = order_pages_generator.admin_create_order_approved_page(
                    cls.get_order_by_order_id(order_id))
            else:
                admin = administrator.Admin(sql_requests.get_order_admin(order_id))
                message = order_pages_generator.admin_create_order_unavailable_page(admin, order_id)
        else:
            message = order_pages_generator.admin_create_is_not_admin_page()
        return message

    #  Отменить заказ
    @classmethod
    def close_order(cls, order_id, order_admin):
        global message
        if order_admin is not None:
            if sql_requests.get_order_admin(order_id) is not None:
                admin = administrator.Admin(sql_requests.get_order_admin(order_id))
                if admin.admin_id == order_admin.admin_id:
                    sql_requests.update_order_status(order_id, order_admin.admin_id, cls.order_statuses.CLOSED)
                    message = order_pages_generator.admin_create_order_canceled_page(order_id)
                else:
                    message = order_pages_generator.admin_create_order_unavailable_page(admin, order_id)
            else:
                sql_requests.update_order_status(order_id, order_admin.admin_id, cls.order_statuses.CLOSED)
                message = order_pages_generator.admin_create_order_canceled_page(order_id)
        else:
            message = order_pages_generator.admin_create_is_not_admin_page()
        return message

