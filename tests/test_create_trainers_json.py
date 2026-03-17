from models.trainers import Trainers
from models.trainer import Trainer

tr = Trainers()

# Tạo 10 ông bà HLV tên mới hoàn toàn, chuyên môn khác nhau
tr1 = Trainer("Lý Trọng Bằng", "trongbang123", "trainer", "0981111222", "trongbang.pt@gmail.com", "M", "Gym")
tr2 = Trainer("Trần Thị Hà", "thiha456", "trainer", "0982222333", "ha.yoga@gmail.com", "F", "Yoga")
tr3 = Trainer("Nguyễn Tuấn Anh", "tuananh789", "trainer", "0983333444", "tuananh.boxing@gmail.com", "M", "Boxing")
tr4 = Trainer("Lê Thị Ngọc", "thingoc321", "trainer", "0984444555", "ngoc.pilates@gmail.com", "F", "Pilates")
tr5 = Trainer("Phạm Quốc Việt", "quocviet654", "trainer", "0985555666", "viet.crossfit@gmail.com", "M", "Crossfit")
tr6 = Trainer("Đỗ Minh Khang", "minhkhang987", "trainer", "0986666777", "khang.gym@gmail.com", "M", "Gym")
tr7 = Trainer("Vũ Thu Thảo", "thuthao852", "trainer", "0987777888", "thao.zumba@gmail.com", "F", "Zumba")
tr8 = Trainer("Hoàng Đức Hải", "duchai147", "trainer", "0988888999", "hai.kickboxing@gmail.com", "M", "Kickboxing")
tr9 = Trainer("Ngô Mai Phương", "maiphuong369", "trainer", "0989999000", "phuong.yoga@gmail.com", "F", "Yoga")
tr10 = Trainer("Đinh Trọng Đại", "trongdai258", "trainer", "0980000111", "dai.thehinh@gmail.com", "M", "Thể hình")

# Add cục này vào list
tr.add_items([tr1, tr2, tr3, tr4, tr5, tr6, tr7, tr8, tr9, tr10])

print("Danh sách Huấn luyện viên đã được tạo:")
tr.print_items()

print("\nĐang xuất danh sách ra file trainer.json...")
tr.export_json("../Datasets/trainer.json")
print("Xuất file thành công! Vào kiểm tra lại đi mày.")