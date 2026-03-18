# test_create_booking_json.py
import json
import os

filepath = "../Datasets/booking_history.json"
if not os.path.exists(filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump([], f) # Tạo một danh sách rỗng []
    print("Đã tạo file booking_history.json rỗng thành công!")
else:
    print("File đã tồn tại rồi, không cần tạo nữa.")