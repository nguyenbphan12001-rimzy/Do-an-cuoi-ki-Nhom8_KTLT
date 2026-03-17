from models.rooms import Rooms
from models.room import Room

# Tao set data y chang cái list xổ xuống trong hình của mày
rm = Rooms()
rm.add_items([
    Room("P01", "Phòng Pilates P01", "Pilates"),
    Room("P02", "Phòng Pilates P02", "Pilates"),
    Room("Y01", "Phòng Yoga Master Y01", "Yoga"),
    Room("Y02", "Phòng Yoga Master Y02", "Yoga"),
    Room("B1", "Phòng Boxing B1", "Boxing"),
    Room("B2", "Phòng Boxing B2", "Boxing"),
    Room("KG01", "Không gian chung", "Tự do")
])

print("Đang xuất danh sách phòng ra file room.json...")
rm.export_json("../Datasets/room.json")
print("Tạo file room.json thành công!")