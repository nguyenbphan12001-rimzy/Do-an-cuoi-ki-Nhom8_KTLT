class Member:
    def __init__(self,username=None, id=None,phone_number=None,gender=None,serve=None,expire_date=None):
        self.username = username
        self.id=id
        self.phone_number=phone_number
        self.gender = gender
        self.serve=serve
        self.expire_date=expire_date
    def __str__(self):
        infor = f"{self.username}\t{self.id}\t{self.phone_number}\t{self.gender}\t{self.serve}\t{self.expire_date}"
        return infor