# booking.py
import datetime

from bson.objectid import ObjectId


class Booking:
    ID = "id"
    USER_ID = "user_id"
    RESTAURANT_ID = "restaurant_id"
    NUM_PEOPLE = "num_people"
    DATE = "date"
    TIME = "time"
    CREATED_DATE_TIME = "created_date_time"

    def __init__(
            self,
            user_id: str,
            restaurant_id: str,
            num_people: int,
            date: str,
            time: str = None,
            created_date_time: datetime.datetime = None,
            booking_id: str = None,
    ):
        self.id = booking_id if booking_id else f"bid_{ObjectId()}"
        self.user_id = user_id
        self.restaurant_id = restaurant_id
        self.num_people = num_people
        self.date = date
        self.time = time
        self.created_date_time = created_date_time or datetime.datetime.now()

    def to_dict(self):
        return {
            Booking.ID: self.id,
            Booking.USER_ID: self.user_id,
            Booking.RESTAURANT_ID: self.restaurant_id,
            Booking.NUM_PEOPLE: self.num_people,
            Booking.DATE: self.date,
            Booking.TIME: self.time,
            Booking.CREATED_DATE_TIME: self.created_date_time.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data[Booking.USER_ID],
            restaurant_id=data[Booking.RESTAURANT_ID],
            num_people=data[Booking.NUM_PEOPLE],
            date=data[Booking.DATE],
            time=data[Booking.TIME],
            created_date_time=datetime.datetime.fromisoformat(data[Booking.CREATED_DATE_TIME]),
            booking_id=data[Booking.ID],
        )

    def copy(self):
        return Booking(
            user_id=self.user_id,
            restaurant_id=self.restaurant_id,
            num_people=self.num_people,
            date=self.date,
            time=self.time,
            created_date_time=self.created_date_time,
            booking_id=self.id,
        )
