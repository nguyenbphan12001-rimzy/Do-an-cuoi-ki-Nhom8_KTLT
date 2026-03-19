from models.rooms import Rooms
from models.room import Room

# Tao set data y chang cái list xổ xuống trong hình của mày
rm = Rooms()
rm.add_items([
    Room("P01", "Phòng Pilates P01", "Pilates",0,20),
    Room("P02", "Phòng Pilates P02", "Pilates",0,20),
    Room("Y01", "Phòng Yoga Master Y01", "Yoga",0,20),
    Room("Y02", "Phòng Yoga Master Y02", "Yoga",0,15),
    Room("B1", "Phòng Boxing B1", "Boxing",0,20),
    Room("B2", "Phòng Boxing B2", "Boxing",0,20),
    Room("KG01", "Không gian chung", "Tự do",0,50)
])

print("Đang xuất danh sách phòng ra file room.json...")
rm.export_json("../Datasets/room.json")
print("Tạo file room.json thành công!")