from models.users import Users

us = Users()
us.import_json("../Datasets/user.json")
print("Danh sách khách hàng đã tham gia đặt lịch:")
us.print_items()