from typing import List, Dict

from submodules.database.connectors.mongo_connector import db
from submodules.database.data_models.restaurant import Restaurant


class RestaurantRepository:
    def __init__(self):
        self.collection = db["restaurants"]

    def insert_restaurant(self, restaurant: Restaurant):
        restaurant_id = self.collection.insert_one(restaurant.to_dict()).inserted_id
        return restaurant_id

    def find_restaurant_by_id(self, restaurant_id: str):
        restaurant_data = self.collection.find_one({"id": restaurant_id})
        if restaurant_data:
            return Restaurant.from_dict(restaurant_data)
        return None

    def get_all_restaurants(self, limit: int = 10, offset: int = 0):
        cursor = self.collection.find().skip(offset).limit(limit)
        restaurants = [Restaurant.from_dict(doc) for doc in cursor]
        return restaurants

    def get_restaurants_by_ids(self, restaurant_ids: List[str]) -> Dict[str, Restaurant]:
        cursor = self.collection.find({"id": {"$in": restaurant_ids}})
        restaurants = {doc["id"]: Restaurant.from_dict(doc) for doc in cursor}
        return restaurants

    def get_restaurants_by_cuisine(self, cuisine: str, limit: int = 10, offset: int = 0):
        cursor = self.collection.find({"cuisine": cuisine}).skip(offset).limit(limit)
        restaurants = [Restaurant.from_dict(doc) for doc in cursor]
        return restaurants

    def get_unique_cuisines(self, limit: int = 10, offset: int = 0):
        pipeline = [
            {"$group": {"_id": "$cuisine"}},
            {"$skip": offset},
            {"$limit": limit}
        ]
        results = self.collection.aggregate(pipeline)
        cuisines = [doc['_id'] for doc in results]
        return cuisines

    def get_unique_cuisines_ordered(self, limit: int = 10, offset: int = 0):
        pipeline = [
            {"$group": {"_id": "$cuisine", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$skip": offset},
            {"$limit": limit}
        ]
        results = self.collection.aggregate(pipeline)
        cuisines = [doc['_id'] for doc in results]
        return cuisines
