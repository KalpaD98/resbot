from submodules.database.connectors.mongo_connector import db

from submodules.database.models.booking import Booking


class BookingRepository:
    def __init__(self):
        self.bookings_collection = db["bookings"]

    def insert_booking(self, booking: Booking):
        booking_id = self.bookings_collection.insert_one(booking.to_dict()).inserted_id
        return booking_id

    def find_booking_by_id(self, booking_id: str):
        booking_data = self.bookings_collection.find_one({"id": booking_id})
        if booking_data:
            return Booking.from_dict(booking_data)
        return None

    def find_all_bookings(self, limit: int = 10):
        cursor = self.bookings_collection.find().limit(limit)
        bookings = [Booking.from_dict(doc) for doc in cursor]
        return bookings

    def get_bookings_by_user_id(self, user_id: str, limit: int = 10):
        cursor = self.bookings_collection.find({"user.id": user_id}).limit(limit)
        bookings = [Booking.from_dict(doc) for doc in cursor]
        return bookings

    def get_bookings_by_restaurant_id(self, restaurant_id: str, limit: int = 10):
        cursor = self.bookings_collection.find({"restaurant.id": restaurant_id}).limit(limit)
        bookings = [Booking.from_dict(doc) for doc in cursor]
        return bookings

    def modify_booking(self, booking_id: str, date: str = None, time: str = None, num_people: int = None):
        update_data = {}
        if date:
            update_data["date"] = date
        if time:
            update_data["time"] = time
        if num_people:
            update_data["num_people"] = num_people

        self.bookings_collection.update_one({"id": booking_id}, {"$set": update_data})

    def cancel_booking(self, booking_id: str):
        self.bookings_collection.delete_one({"id": booking_id})
