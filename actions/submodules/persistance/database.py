# database.py
from pymongo import MongoClient

from actions.submodules.entities.booking import Booking
from actions.submodules.entities.restaurant import Restaurant
from actions.submodules.entities.user import User

# Replace "mongodb://localhost:27017" with the connection string to your MongoDB server
client = MongoClient("mongodb://localhost:27017")
db = client["rasa_chatbot"]


def save_user(user: User) -> None:
    db.users.insert_one(user.__dict__)


def save_restaurant(restaurant: Restaurant) -> None:
    db.restaurants.insert_one(restaurant.__dict__)


def save_booking(booking: Booking) -> None:
    db.bookings.insert_one(booking.__dict__)

# ---------- add below to all_actions for saving data to database ----------
#
# from database import save_user, save_restaurant, save_booking
#
# class ActionSaveUserAndCompleteRegistration(Action):
#     def name(self) -> Text:
#         return "action_save_user_and_complete_registration"
#
#     async def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#
#         user_name = tracker.get_slot("user_name")
#         user_email = tracker.get_slot("user_email")
#         password = tracker.get_slot("password")
#
#         # Save user to the database
#         new_user = User(name=user_name, email=user_email, password=password)
#         save_user(new_user)
#
#         # Your other logic here
#         # ...
#
#         return []

# for saving booking data to database #

# from database import save_user, save_restaurant, save_booking
#
# # ...
#
# class ActionSaveBooking(Action):
#     def name(self) -> Text:
#         return "action_save_booking"
#
#     async def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#
#         user_id = tracker.get_slot("user_id")
#         restaurant_id = tracker.get_slot("restaurant_id")
#         date = tracker.get_slot("date")
#         num_people = tracker.get_slot("num_people")
#         time = tracker.get_slot("time")
#
#         # Fetch the user and restaurant objects from the database, or from other sources if needed
#         user = get_user_by_id(user_id)
#         restaurant = get_restaurant_by_id(restaurant_id)
#
#         # Save booking to the database
#         new_booking = Booking(user=user, restaurant=restaurant, date=date, num_people=num_people, time=time)
#         save_booking(new_booking)
#
#         # Your other logic here, e.g., sending a confirmation message
#         # ...
#
#         return []

# domain.yml
#
# all_actions:
#   - action_save_booking

# rules.yml or stories.yml

# - rule: Save booking
#   steps:
#     - intent: confirm_booking
#     - action: action_save_booking
