class Trainer:
    def __init__(self, username="", password="", role="trainer",
                 phone_number="", email="", gender="", status="",
                 available_dates=None, available_times=None): # 🔥 Thêm 2 cái này
        self.username = username
        self.password = password
        self.role = role
        self.phone_number = phone_number
        self.email = email
        self.gender = gender
        self.status = status
        # Nếu không truyền vào thì mặc định là list rỗng
        self.available_dates = available_dates if available_dates is not None else []
        self.available_times = available_times if available_times is not None else []

    def __str__(self):
        return f"{self.username} | {self.role} | {self.phone_number}"

    # 🔥 convert từ JSON → object
    @staticmethod
    def from_dict(data: dict):
        return Trainer(
            username=data.get("username", ""),
            password=data.get("password", ""),
            role=data.get("role", "trainer"), # Mặc định là trainer
            phone_number=data.get("phone_number", ""),
            email=data.get("email", ""),
            gender=data.get("gender", ""),
            status=data.get("status", ""),
            available_dates=data.get("available_dates", []), # 🔥 Lấy data từ JSON
            available_times=data.get("available_times", [])  # 🔥 Lấy data từ JSON
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
            "status": self.status,
            "available_dates": self.available_dates, # 🔥 Ghi data ra JSON
            "available_times": self.available_times  # 🔥 Ghi data ra JSON
        }