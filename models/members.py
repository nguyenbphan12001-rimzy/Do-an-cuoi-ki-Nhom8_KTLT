import json

from models.Mycollections import MyCollections
from models.member import Member


class Members (MyCollections):
    def export_json(self, filename):
        self.filename = filename
        data = {'Datasets': [member.to_dict() for member in self.list]}

        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

    def import_json(self, filename):
        self.filename = filename
        self.list.clear()
        try:
            with open(filename, encoding="utf-8") as json_file:
                data = json.load(json_file)

                for item in data.get("Datasets", []):
                    member = Member.from_dict(item)
                    self.add_item(member)
        except FileNotFoundError:
            print("File không tồn tại")
        except Exception as e:
            print("Lỗi đọc file:", e)
    def find_item(self, itemId):
        item = None
        for it in self.list:
            if it.username == itemId:
                item = it
                break
        return item

    def save_item(self, item):
        exit_item = self.find_item(item.username)
        if exit_item == None:
            self.add_item(item)
        else:
            exit_item.username = item.username
            exit_item.phone_number = item.phone_number
            exit_item.gender = item.gender
            exit_item.package=item.package
            exit_item.register_date=item.register_date
            exit_item.expire_date=item.expire_date
        self.export_json(self.filename)

    def remove_item(self, itemId):
        item = self.find_item(itemId)
        if item == None:
            return False
        self.list.remove(item)
        self.export_json(self.filename)
        return True

