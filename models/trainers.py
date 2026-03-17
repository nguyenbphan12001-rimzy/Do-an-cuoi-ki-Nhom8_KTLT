import json
from models.Mycollections import MyCollections
from models.trainer import Trainer

class Trainers(MyCollections):

    # 📤 EXPORT JSON
    def export_json(self, filename):
        self.filename = filename
        data = {"Datasets": [trainer.to_dict() for trainer in self.list]}

        with open(filename, "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

    # 📥 IMPORT JSON
    def import_json(self, filename):
        self.filename = filename
        self.list.clear()

        try:
            with open(filename, encoding="utf-8") as json_file:
                data = json.load(json_file)

                for item in data.get("Datasets", []):
                    trainer = Trainer.from_dict(item)   # 🔥 Đổi thành Trainer
                    self.add_item(trainer)

        except FileNotFoundError:
            print("File JSON của HLV không tồn tại")
        except Exception as e:
            print("Lỗi đọc file HLV:", e)

    # 🔍 TÌM HLV
    def find_item(self, username):
        for trainer in self.list:
            if trainer.username == username:
                return trainer
        return None

    # 💾 SAVE / UPDATE HLV
    def save_item(self, trainer):
        exist_trainer = self.find_item(trainer.username)

        if exist_trainer is None:
            self.add_item(trainer)
        else:
            exist_trainer.password = trainer.password
            exist_trainer.role = trainer.role
            exist_trainer.phone_number = trainer.phone_number
            exist_trainer.email = trainer.email
            exist_trainer.gender = trainer.gender
            exist_trainer.status = trainer.status

        self.export_json(self.filename)

    # ❌ XOÁ HLV
    def remove_item(self, username):
        trainer = self.find_item(username)

        if trainer is None:
            return False

        self.list.remove(trainer)
        self.export_json(self.filename)
        return True