import logging
from typing import List, Dict, Optional

from pymongo.errors import PyMongoError

from submodules.database.connectors.mongo_connector import db
from submodules.database.data_models.restaurant import Restaurant
from submodules.other_modules.recommendation import get_business_ids


class RestaurantRepository:
    """
    Repository class for handling restaurant related database operations.
    """

    def __init__(self):
        self.collection = db["restaurants"]

    def insert_restaurant(self, restaurant: Restaurant) -> str:
        """
        Insert a restaurant into the database.

        :param restaurant: Restaurant object to insert
        :return: Inserted restaurant's ID
        """
        try:
            restaurant_id = self.collection.insert_one(restaurant.to_dict()).inserted_id
            return restaurant_id
        except PyMongoError as e:
            raise Exception(f"Error inserting restaurant: {e}")

    def find_restaurant_by_id(self, restaurant_id: str) -> Optional[Restaurant]:
        """
        Find a restaurant by ID.

        :param restaurant_id: ID of the restaurant to find
        :return: Restaurant object if found, None otherwise
        """
        try:
            restaurant_data = self.collection.find_one({"id": restaurant_id})
            if restaurant_data:
                return Restaurant.from_dict(restaurant_data)
            return None
        except PyMongoError as e:
            raise Exception(f"Error finding restaurant by ID: {e}")

    def get_all_restaurants(self, limit: int = 10, offset: int = 0) -> List[Restaurant]:
        """
        Get a list of all restaurants with pagination.

        :param limit: Number of restaurants to retrieve
        :param offset: Offset for the query (pagination)
        :return: List of Restaurant objects
        """
        try:
            cursor = self.collection.find().skip(offset).limit(limit)
            return [Restaurant.from_dict(doc) for doc in cursor]
        except PyMongoError as e:
            raise Exception(f"Error retrieving all restaurants: {e}")

    def get_restaurants_by_ids(self, restaurant_ids: List[str]) -> Dict[str, Restaurant]:
        """
        Get a dictionary of restaurants by their IDs.

        :param restaurant_ids: List of restaurant IDs to retrieve
        :return: Dictionary of Restaurant objects with their ID as the key
        """
        try:
            cursor = self.collection.find({"id": {"$in": restaurant_ids}})
            return {doc["id"]: Restaurant.from_dict(doc) for doc in cursor}
        except PyMongoError as e:
            raise Exception(f"Error retrieving restaurants by IDs: {e}")

    def get_restaurants_filter_by_cuisine(self, cuisine: str, limit: int = 10, offset: int = 0) -> List[Restaurant]:
        """
        Get a list of restaurants by cuisine with pagination.

        :param cuisine: Cuisine type to filter by
        :param limit: Number of restaurants to retrieve
        :param offset: Offset for the query (pagination)
        :return: List of Restaurant objects
        """
        try:
            # Use the aggregation pipeline to add a new field
            pipeline = [
                {
                    "$addFields": {
                        "cuisine_categories": {"$concatArrays": ["$categories", ["$cuisine"]]}
                    }
                },
                {
                    "$match": {
                        "cuisine_categories": cuisine
                    }
                },
                {
                    "$skip": offset
                },
                {
                    "$limit": limit
                }
            ]
            cursor = self.collection.aggregate(pipeline)
            return [Restaurant.from_dict(doc) for doc in cursor]
        except PyMongoError as e:
            raise Exception(f"Error retrieving restaurants by cuisine: {e}")

    def get_unique_cuisines_ordered(self, limit: int = 7, offset: int = 0) -> List[str]:
        """
        Get a list of unique cuisines ordered by count with pagination.

        :param limit: Number of cuisines to retrieve
        :param offset: Offset for the query (pagination)
        :return: List of unique cuisine types
        """
        try:
            pipeline = [
                {"$group": {"_id": "$cuisine", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$skip": offset},
                {"$limit": limit}
            ]
            results = self.collection.aggregate(pipeline)
            return [doc['_id'] for doc in results]
        except PyMongoError as e:
            raise Exception(f"Error retrieving unique cuisines ordered: {e}")

    """
        get restaurants from recommendation module
        get a list of business_ids' from recommendation module
        use business_ids' to get restaurants from database
    """

    def get_restaurants_with_recommendation_module(self, limit: int = 10, cuisine: str = None, offset: int = 0) -> \
            List[Restaurant]:
        """
        Get a list of restaurants by business_ids from the recommendation module, filtered by cuisine.

        :param limit: Maximum number of restaurants to retrieve (default: 10)
        :param cuisine: Cuisine type to filter the restaurants (optional)
        :param offset: Offset for the query (pagination)
        :return: List of Restaurant objects
        """
        logging.info(f"Getting restaurants from recommendation module with cuisine={cuisine}")
        user_id = "V1AMJ5p050XTl2PZB13YfQ"
        business_ids = get_business_ids(user_id)

        try:
            filter_query = {"business_id": {"$in": business_ids}}
            if cuisine:
                filter_query["cuisine"] = cuisine
            cursor = self.collection.find(filter_query).skip(offset).limit(limit)
            return [Restaurant.from_dict(doc) for doc in cursor]
        except PyMongoError as e:
            raise Exception(f"Error retrieving restaurants by business_ids: {e}")
