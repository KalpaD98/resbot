from actions.submodules.utils.mock_data_utils import users


class User:
    user_count = len(users)

    def __init__(self, name: str, email: str, password: str):
        User.user_count += 1
        self.id = f"uid_{User.user_count}"
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return f"User(id='{self.id}', name='{self.name}', email='{self.email}', password='{self.password}')"

    def __str__(self) -> str:
        return f"User ID: {self.id}, Name: {self.name}, Email: {self.email}"
