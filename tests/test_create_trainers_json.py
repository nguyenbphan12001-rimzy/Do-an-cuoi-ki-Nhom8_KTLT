from models.trainers import Trainers
from models.trainer import Trainer

tr = Trainers()

# Chỉ dùng 4 môn: Tự do, Yoga, Pilates, Boxing
tr1 = Trainer("Lý Trọng Bằng", "trongbang123", "trainer", "0981111222", "trongbang.pt@gmail.com", "M", "Tự do",
              ["18/03/2026", "20/03/2026", "22/03/2026"], ["7h - 9h", "17h - 19h"])
tr2 = Trainer("Trần Thị Hà", "thiha456", "trainer", "0982222333", "ha.yoga@gmail.com", "F", "Yoga",
              ["18/03/2026", "19/03/2026", "21/03/2026"], ["5h - 7h", "15h - 17h"])
tr3 = Trainer("Nguyễn Tuấn Anh", "tuananh789", "trainer", "0983333444", "tuananh.boxing@gmail.com", "M", "Boxing",
              ["19/03/2026", "20/03/2026", "22/03/2026"], ["9h - 11h", "19h - 21h"])
tr4 = Trainer("Lê Thị Ngọc", "thingoc321", "trainer", "0984444555", "ngoc.pilates@gmail.com", "F", "Pilates",
              ["18/03/2026", "21/03/2026", "22/03/2026"], ["7h - 9h", "13h - 15h"])
tr5 = Trainer("Phạm Quốc Việt", "quocviet654", "trainer", "0985555666", "viet.crossfit@gmail.com", "M", "Tự do",
              ["20/03/2026", "21/03/2026", "23/03/2026"], ["15h - 17h", "19h - 21h"])
tr6 = Trainer("Đỗ Minh Khang", "minhkhang987", "trainer", "0986666777", "khang.gym@gmail.com", "M", "Tự do",
              ["18/03/2026", "19/03/2026", "21/03/2026"], ["9h - 11h", "13h - 15h", "17h - 19h"])
tr7 = Trainer("Vũ Thu Thảo", "thuthao852", "trainer", "0987777888", "thao.zumba@gmail.com", "F", "Yoga",
              ["22/03/2026", "24/03/2026", "18/03/2026"], ["17h - 19h", "19h - 21h", "5h - 7h"])
tr8 = Trainer("Hoàng Đức Hải", "duchai147", "trainer", "0988888999", "hai.kickboxing@gmail.com", "M", "Boxing",
              ["19/03/2026", "20/03/2026", "25/03/2026"], ["5h - 7h", "7h - 9h"])
tr9 = Trainer("Ngô Mai Phương", "maiphuong369", "trainer", "0989999000", "phuong.yoga@gmail.com", "F", "Pilates",
              ["18/03/2026", "20/03/2026", "22/03/2026"], ["9h - 11h", "15h - 17h"])
tr10 = Trainer("Đinh Trọng Đại", "trongdai258", "trainer", "0980000111", "dai.thehinh@gmail.com", "M", "Tự do",
               ["21/03/2026", "22/03/2026", "18/03/2026"], ["13h - 15h", "17h - 19h", "7h - 9h"])

tr.add_items([tr1, tr2, tr3, tr4, tr5, tr6, tr7, tr8, tr9, tr10])

print("\nĐang xuất danh sách ra file trainer.json...")
tr.export_json("../Datasets/trainer.json")
print("Cập nhật lại HLV chuẩn 4 môn thành công!")