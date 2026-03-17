# class User:
#     def __init__(self,username=None,password=None,role=None, phone_number=None, email=None, gender=None, status=None):
#         self.username = username
#         self.password = password
#         self.phone_number = phone_number
#         self.email = email
#         self.gender = gender
#         self.status = status
#         self.role = role
#     def __str__(self):
#         infor = f"{self.username}\t{self.password}\t{self.role}\t{self.phone_number}\t{self.email}\t{self.gender}\t{self.status}"
#         return infor

class User:
    def __init__(self, username="", password="", role="user",
                 phone_number="", email="", gender="", status=""):
        self.username = username
        self.password = password
        self.role = role
        self.phone_number = phone_number
        self.email = email
        self.gender = gender
        self.status = status

    def __str__(self):
        return f"{self.username} | {self.role} | {self.phone_number}"

    # 🔥 convert từ JSON → object
    @staticmethod
    def from_dict(data: dict):
        return User(
            username=data.get("username", ""),
            password=data.get("password", ""),
            role=data.get("role", "user"),
            phone_number=data.get("phone_number", ""),
            email=data.get("email", ""),
            gender=data.get("gender", ""),
            status=data.get("status", "")
        )

    # 🔥 convert object → JSON
    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "phone_number": self.phone_number,
            "email": self.email,
            "gender": self.gender,
            "status": self.status
        }