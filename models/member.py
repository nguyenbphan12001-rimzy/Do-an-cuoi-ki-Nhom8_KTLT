class Member:
    def __init__(self,username=None,phone_number=None,gender=None,package=None,register_date=None,expire_date=None):
        self.username = username
        self.phone_number=phone_number
        self.gender = gender
        self.package=package
        self.register_date=register_date
        self.expire_date=expire_date
    def __str__(self):
        infor = f"{self.username}\t{self.phone_number}\t{self.gender}\t{self.package}\t{self.register_date}\t{self.expire_date}"
        return infor

    @staticmethod
    def from_dict(data: dict):
        return Member(
            username=data.get("username", ""),
            phone_number=data.get("phone_number", ""),
            gender=data.get("gender", ""),
            package=data.get("package", ""),
            register_date=data.get("register_date", ""),
            expire_date=data.get("expire_date", "")
        )

    def to_dict(self):
        return {
            "username": self.username,
            "phone_number": self.phone_number,
            "gender": self.gender,
            "package": self.package,
            "register_date": self.register_date,
            "expire_date": self.expire_date
        }