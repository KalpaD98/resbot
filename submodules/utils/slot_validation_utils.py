import datetime
import re
from datetime import datetime, timedelta
from typing import Tuple

from dateutil import parser
from rasa_sdk import Tracker

from actions.all_actions.helper_functions.response_generator.constants import LANGUAGE, SIN
from submodules.database.repositories.user_repository import UserRepository


class SlotValidators:
    @staticmethod
    def validate_date(date_entity: str, tracker: Tracker) -> (bool, str, str):

        language = tracker.get_slot(LANGUAGE)

        if date_entity:
            try:
                date_obj = parser.parse(date_entity).date()
            except ValueError:
                message = "I couldn't understand the date you provided. It seems to be invalid."
                if language == SIN:
                    message = "ඔබ ලබා දුන් දිනය වැරදි. කරුණාකර නිවැරදි දිනයක් ලබා දෙන්න."
                return False, "", message

            today = datetime.now().date()
            tomorrow = today + timedelta(days=1)

            if date_obj >= tomorrow:
                return True, date_obj.isoformat(), ""
            else:
                message = "Please provide a date that is tomorrow or later."
                if language == SIN:
                    message = "කරුණාකර හෙට හෝ හෙටට පසු දිනයක් ලබා දෙන්න."
                return False, "", message
        else:
            message = "I couldn't understand the date you provided. It seems to be invalid."
            if language == SIN:
                message = "ඔබ ලබා දුන් දිනය වැරදි. කරුණාකර නිවැරදි දිනයක් ලබා දෙන්න."
            return False, "", message

    @staticmethod
    def validate_restaurant_id(restaurant_id: str, tracker: Tracker) -> Tuple[bool, str]:
        language = tracker.get_slot(LANGUAGE)
        if restaurant_id.startswith("rid"):
            return True, ""
        else:
            return False, "Restaurant ID should start with 'rid'. Please provide a valid restaurant ID."

    @staticmethod
    def validate_num_people(num_people: str, tracker: Tracker) -> Tuple[bool, str]:
        language = tracker.get_slot(LANGUAGE)
        try:
            num = int(num_people)
            if num > 0:
                return True, ""
            else:
                return False, "The number of people should be greater than 0. Please provide a valid number."
        except ValueError:
            return False, "Please provide a valid number for the number of people."

    @staticmethod
    def validate_cuisine(cuisine: str, tracker: Tracker) -> Tuple[bool, str]:
        language = tracker.get_slot(LANGUAGE)
        supported_cuisines = ["Italian", "Chinese", "Indian", "Mexican", "Japanese"]
        if cuisine.lower() in [c.lower() for c in supported_cuisines]:
            return True, ""
        else:
            return False, f"Please provide a valid cuisine type. Supported cuisines are: {', '.join(supported_cuisines)}."

    @staticmethod
    def validate_user_id(user_id: str, tracker: Tracker) -> Tuple[bool, str]:
        language = tracker.get_slot(LANGUAGE)
        if user_id.startswith("uid"):
            return True, ""
        else:
            return False, "User ID should start with 'uid'. Please provide a valid user ID."

    @staticmethod
    def validate_user_name(user_name: str, tracker: Tracker) -> Tuple[bool, str, str]:
        language = tracker.get_slot(LANGUAGE)
        user_name = user_name.strip()
        if len(user_name) >= 3:
            return True, user_name, ""
        else:
            return False, "", "Please provide a username with at least 3 characters."

    @staticmethod
    def validate_email(email: str, tracker: Tracker) -> Tuple[bool, str, str]:
        language = tracker.get_slot(LANGUAGE)
        email = email.strip()
        if email:
            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if re.match(email_regex, email):
                # check if email is already registered
                user_repository = UserRepository()
                user = user_repository.find_user_by_email(email)
                if user:
                    return False, "", "This email is already registered. Please provide a different email."
                return True, email, ""
            else:
                return False, "", "Please provide a valid email address."
        else:
            return False, "", "Please provide a valid email address."

    @staticmethod
    def validate_password(password: str, tracker: Tracker) -> Tuple[bool, str, str]:
        language = tracker.get_slot(LANGUAGE)
        password = password.strip()
        if len(password) >= 4:
            return True, password, ""
        else:
            return False, "", "Please provide a password with at least 4 characters."

    @staticmethod
    def validate_time(time: str, tracker: Tracker) -> Tuple[bool, str, str]:
        language = tracker.get_slot(LANGUAGE)
        try:
            time_obj = datetime.datetime.strptime(time, "%H:%M")
            formatted_time = time_obj.strftime("%H:%M")
            return True, formatted_time, ""
        except ValueError:
            try:
                time_obj = datetime.datetime.strptime(time, "%I:%M %p")
                formatted_time = time_obj.strftime("%H:%M")
                return True, formatted_time, ""
            except ValueError:
                return False, "", "Please provide a valid time in either 24-hour format (e.g., '14:30' or '06:15') or " \
                                  "12-hour format (e.g., '2:30 PM' or '6:15 AM')."

    @staticmethod
    def validate_booking_id(booking_reference_id: str, tracker: Tracker) -> Tuple[bool, str]:
        language = tracker.get_slot(LANGUAGE)
        if booking_reference_id.startswith("bid_"):
            return True, ""
        else:
            return False, "Please select a valid booking."
