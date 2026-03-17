class Room:
    def __init__(self, room_id, name, category):
        self.room_id = room_id
        self.name = name
        self.category = category  # "Yoga", "Pilates", "Boxing", "Tự do"

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "name": self.name,
            "category": self.category
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["room_id"], data["name"], data["category"])