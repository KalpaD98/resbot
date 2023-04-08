from database.connectors.mongo_connector import db

from database.models.user import User


class UserRepository:
    def __init__(self):
        self.users_collection = db["users"]

    def insert_user(self, user: User):
        user_id = self.users_collection.insert_one(user.to_dict()).inserted_id
        return user_id

    def find_user_by_email(self, email: str):
        user_data = self.users_collection.find_one({"email": email})
        if user_data:
            return User.from_dict(user_data)
        return None
