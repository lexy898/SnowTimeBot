from datetime import datetime
from order import order_management
import sql_requests


class Accessory:
    def __init__(self, accessory_db):
        self.id = accessory_db['ID']
        self.name = accessory_db['NAME']
        self.type = accessory_db['TYPE']
        self.picture_url = accessory_db['PICTURE_URL']
        self.size = accessory_db['SIZE']
        self.growth = accessory_db['GROWTH']
        self.start_date = accessory_db['START_DATE']
        self.end_date = accessory_db['END_DATE']
        self.order_id = accessory_db['ORDER_ID']

    def accessory_availability(self, date):
        if self.start_date is None or self.end_date is None:
            return True
        start_date = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(self.end_date, "%Y-%m-%d %H:%M:%S")
        current_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        start_delta = (start_date - current_date).days
        end_delta = (end_date - current_date).days
        if (start_delta <= 0) and (end_delta > 0):
            statuses = order_management.OrderStatuses()
            current_order_status = sql_requests.get_order_status(self.order_id)
            if current_order_status != statuses.CLOSED:
                return False
        else:
            return True
