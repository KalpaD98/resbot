from database.connectors.mongo_connector import db

from database.models.booking import Booking


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
