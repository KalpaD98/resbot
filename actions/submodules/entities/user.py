import random
import string


class User:

    def __init__(self, name: str, email: str, password: str):
        self.id = f"uid_{User.generate_random_string()}"
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return f"User(id='{self.id}', name='{self.name}', email='{self.email}', password='{self.password}')"

    def __str__(self) -> str:
        return f"User ID: {self.id}, Name: {self.name}, Email: {self.email}"

    @staticmethod
    def generate_random_string(length=8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
