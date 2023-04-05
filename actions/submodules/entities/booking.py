import datetime

from actions.submodules.entities.restaurant import Restaurant
from actions.submodules.entities.user import User


class Booking:
    booking_count = 0

    def __init__(
            self,
            user: User,
            restaurant: Restaurant,
            num_people: int,
            date: str,
            time: str = None,
            created_date_time: datetime.datetime = None,
    ):
        Booking.booking_count += 1
        self.id = f"bid_{Booking.booking_count}"
        self.user = user
        self.restaurant = restaurant
        self.num_people = num_people
        self.date = date
        self.time = time
        self.created_date_time = created_date_time or datetime.datetime.now()

    def __repr__(self) -> str:
        return f"Booking(id='{self.id}', user='{self.user.name}', restaurant='{self.restaurant.name}', date='{self.date}', time='{self.time}', num_people={self.num_people})"

    def __str__(self) -> str:
        return f"Booking ID: {self.id}, User: {self.user.name}, Restaurant: {self.restaurant.name}, Date: {self.date}, Time: {self.time}, Num People: {self.num_people}"
