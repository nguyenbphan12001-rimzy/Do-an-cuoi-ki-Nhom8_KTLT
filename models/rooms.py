import json
import os
from models.room import Room

class Rooms:
    def __init__(self):
        self.list = []

    def add_items(self, items):
        self.list.extend(items)

    def export_json(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump([room.to_dict() for room in self.list], f, indent=4, ensure_ascii=False)

    def import_json(self, filepath):
        if not os.path.exists(filepath):
            print(f"Không tìm thấy file {filepath}")
            return
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.list = [Room.from_dict(item) for item in data]