class Room:
    def __init__(self, room_id=None, name=None, category=None,current_user=None):
        self.room_id = room_id
        self.name = name
        self.category = category
        self.current_user= current_user

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "name": self.name,
            "category": self.category,
            "current_user": self.current_user
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["room_id"], data["name"], data["category"], data["current_user"])