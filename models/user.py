class User:
    def __init__(self,username=None,password=None, phone_number=None, email=None, gender=None, status=None):
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.email = email
        self.gender = gender
        self.status = status
    def __str__(self):
        infor = f"{self.username}\t{self.password}\t{self.phone_number}\t{self.email}\t{self.gender}\t{self.status}"
        return infor