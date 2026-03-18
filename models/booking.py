class Booking:
    def __init__(self, booking_id, username, room_id, time_slot, date):
        self.booking_id = booking_id
        self.username = username
        self.room_id = room_id
        self.time_slot = time_slot
        self.date = date

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "username": self.username,
            "room_id": self.room_id,
            "time_slot": self.time_slot,
            "date": self.date
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["booking_id"], data["username"], data["room_id"], data["time_slot"], data["date"])