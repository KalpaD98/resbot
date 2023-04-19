# user.py
from bson.objectid import ObjectId


class User:
    ID = "id"
    NAME = "name"
    EMAIL = "email"
    PASSWORD = "password"

    def __init__(self, name: str, email: str, password: str, user_id: str = None):
        self.id = user_id if user_id else f"uid_{ObjectId()}"
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return f"User(id='{self.id}', name='{self.name}', email='{self.email}', password='{self.password}')"

    def __str__(self) -> str:
        return f"User ID: {self.id}, Name: {self.name}, Email: {self.email}"

    def to_dict(self):
        return {
            User.ID: self.id,
            User.NAME: self.name,
            User.EMAIL: self.email,
            User.PASSWORD: self.password,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data[User.NAME],
            email=data[User.EMAIL],
            password=data[User.PASSWORD],
            user_id=data[User.ID],
        )
