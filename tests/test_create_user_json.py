from models.users import Users
from models.user import User

us = Users()
us1 = User("Lâm Tâm Như", "lamtamnhu123", "0911172457", "nhulam123@gmail.com","F", "Không")
us2 = User("Nguyễn Minh Anh", "minhanh456", "0912345678", "minhanh@gmail.com", "F", "Yoga 1")
us3 = User("Trần Quốc Bảo", "quocbao789", "0913456789", "quocbao@gmail.com", "M", "Tự do")
us4 = User("Phạm Gia Huy", "giahuy321", "0914567890", "giahuy@gmail.com", "M", "Không")
us5 = User("Lê Thu Trang", "thutrang654", "0915678901", "thutrang@gmail.com", "F", "Boxing 1")
us6 = User("Võ Hoàng Nam", "hoangnam987", "0916789012", "hoangnam@gmail.com", "M", "Không")
us7 = User("Đặng Ngọc Lan", "ngoclan852", "0917890123", "ngoclan@gmail.com", "F", "Pilates")
us8 = User("Bùi Thanh Tùng", "thanhtung147", "0918901234", "thanhtung@gmail.com", "M", "Không")
us9 = User("Phan Mỹ Linh", "mylinh369", "0919012345", "mylinh@gmail.com", "F", "Không")
us10 = User("Đỗ Đức Anh", "ducanh258", "0910123456", "ducanh@gmail.com", "M", "Không")

us.add_items([us1, us2, us3, us4, us5, us6, us7, us8, us9, us10])
print("Danh sách khách hàng đã tham gia đặt lịch:")
us.print_items()
print("Xuất danh sách ra json file")
us.export_json("../Datasets/user.json")