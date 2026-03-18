# import json
#
# from models.Mycollections import MyCollections
# from models.user import User
#
# class Users (MyCollections):
#     def export_json(self, filename):
#         self.filename = filename
#         data = {'Datasets': []}
#         for item in self.list:
#             data['Datasets'].append({
#                 'username': item.username,
#                 'role': item.role,
#                 'password': item.password,
#                 'phone_number': item.phone_number,
#                 'email': item.email,
#                 'gender': item.gender,
#                 'status': item.status
#             })
#         with open(filename, 'w', encoding='utf-8') as outfile:
#             json.dump(data, outfile, ensure_ascii=False, indent=4)
#
#     def import_json(self, filename):
#         self.filename = filename
#         self.list.clear()
#         with open(filename, encoding='utf-8') as json_file:
#             data = json.load(json_file)
#             for item in data['Datasets']:
#                 username = item["username"]
#                 password = item["password"]
#                 role = item["role"]
#                 phone_number = item["phone_number"]
#                 email = item["email"]
#                 gender = item["gender"]
#                 status = item["status"]
#                 item = User(username,password,role,phone_number,email,gender,status)
#                 self.add_item(item)
#
#     def find_item(self, itemId):
#         item = None
#         for it in self.list:
#             if it.username == itemId:
#                 item = it
#                 break
#         return item
#
#     def save_item(self, item):
#         exit_item = self.find_item(item.username)
#         if exit_item == None:
#             self.add_item(item)
#         else:
#             exit_item.username = item.username
#             exit_item.password = item.password
#             exit_item.role = item.role
#             exit_item.phone_number = item.phone_number
#             exit_item.email = item.email
#             exit_item.gender = item.gender
#             exit_item.status = item.status
#
#         self.export_json(self.filename)
#
#     def remove_item(self, itemId):
#         item = self.find_item(itemId)
#         if item == None:
#             return False
#         self.list.remove(item)
#         self.export_json(self.filename)
#         return True


import json

from models.Mycollections import MyCollections
from models.user import User


class Users(MyCollections):
    def export_json(self, filename):
        self.filename = filename
        data = {"Datasets": [user.to_dict() for user in self.list]}

        with open(filename, "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

    def import_json(self, filename):
        self.filename = filename
        self.list.clear()
        try:
            with open(filename, encoding="utf-8") as json_file:
                data = json.load(json_file)

                for item in data.get("Datasets", []):
                    user = User.from_dict(item)
                    self.add_item(user)
        except FileNotFoundError:
            print("File không tồn tại")
        except Exception as e:
            print("Lỗi đọc file:", e)
    def find_item(self, username):
        for user in self.list:
            if user.username == username:
                return user
        return None
    def save_item(self, user):
        exist_user = self.find_item(user.username)
        if exist_user is None:
            self.add_item(user)
        else:
            exist_user.password = user.password
            exist_user.role = user.role
            exist_user.phone_number = user.phone_number
            exist_user.email = user.email
            exist_user.gender = user.gender
            exist_user.status = user.status

        self.export_json(self.filename)
    def remove_item(self, username):
        user = self.find_item(username)
        if user is None:
            return False
        self.list.remove(user)
        self.export_json(self.filename)
        return True

    #Cập nhật trạng thái thành member
    def upgrade_to_member(self,username):
        user=self.find_item(username)
        if user is None:
            return False
        if user.status=="Member":
            return False
        user.status="Member"
        self.export_json(self.filename)
        return True