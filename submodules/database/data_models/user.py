from typing import List, Optional

from bson.objectid import ObjectId


class User:
    ID = "id"
    NAME = "name"
    EMAIL = "email"
    PASSWORD = "password"
    FAVORITE_CUISINES = "favorite_cuisines"

    def __init__(self, name: str, email: str, password: str, user_id: str = None,
                 favorite_cuisines: Optional[List[str]] = None):
        self.id = user_id if user_id else f"uid_{ObjectId()}"
        self.name = name
        self.email = email
        self.password = password
        self.favorite_cuisines = favorite_cuisines or []

    def __repr__(self) -> str:
        return f"User(id='{self.id}', name='{self.name}', email='{self.email}', password='{self.password}', favorite_cuisines={self.favorite_cuisines})"

    def __str__(self) -> str:
        return f"User ID: {self.id}, Name: {self.name}, Email: {self.email}, Favorite Cuisines: {', '.join(self.favorite_cuisines)}"

    def to_dict(self):
        return {
            User.ID: self.id,
            User.NAME: self.name,
            User.EMAIL: self.email,
            User.PASSWORD: self.password,
            User.FAVORITE_CUISINES: self.favorite_cuisines,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data[User.NAME],
            email=data[User.EMAIL],
            password=data[User.PASSWORD],
            user_id=data[User.ID],
            favorite_cuisines=data.get(User.FAVORITE_CUISINES),
        )
