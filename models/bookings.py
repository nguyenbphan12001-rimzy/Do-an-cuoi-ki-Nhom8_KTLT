import json
import os

from models.Mycollections import MyCollections
from models.booking import Booking

class Bookings(MyCollections):
    def __init__(self):
        self.list = []

    def add_booking(self, booking):
        self.list.append(booking)

    def export_json(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump([b.to_dict() for b in self.list], f, indent=4, ensure_ascii=False)

    def import_json(self, filepath):
        if not os.path.exists(filepath):
            return # File chưa có thì thôi, coi như danh sách rỗng
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.list = [Booking.from_dict(item) for item in data]