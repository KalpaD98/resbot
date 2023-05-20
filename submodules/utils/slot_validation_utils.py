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

        language = LanguageSelector.get_language(tracker)

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
        language = LanguageSelector.get_language(tracker)
        if restaurant_id.startswith("rid"):
            return True, ""
        else:
            message = "Restaurant ID should start with 'rid'. Please provide a valid restaurant ID."
            if language == SIN:
                message = "Restaurant ID 'rid' සඳහා ආරම්භ කිරීම අවශ්‍ය වේ. කරුණාකර නිවැරදි Restaurant ID ලබා දෙන්න."
            return False, message

    @staticmethod
    def validate_num_people(num_people: str, tracker: Tracker) -> Tuple[bool, str]:
        language = LanguageSelector.get_language(tracker)
        try:
            num = int(num_people)
            if num > 0:
                return True, ""
            else:
                message = "The number of people should be greater than 0. Please provide a valid number."
                if language == SIN:
                    message = "පුද්ගලයාගේ ගණන 0 වඩා වැඩි විය යුතුය. කරුණාකර නිවැරදි ගණනක් ලබා දෙන්න."
                return False, message
        except ValueError:
            message = "Please provide a valid number for the number of people."
            if language == SIN:
                message = "කරුණාකර පුද්ගලයාගේ ගණන සඳහා නිවැරදි අංකයක් ලබා දෙන්න."
            return False, message

    @staticmethod
    def validate_cuisine(cuisine: str, tracker: Tracker) -> Tuple[bool, str]:
        language = LanguageSelector.get_language(tracker)
        supported_cuisines = ["Italian", "Chinese", "Indian", "Mexican", "Japanese"]
        if cuisine.lower() in [c.lower() for c in supported_cuisines]:
            return True, ""
        else:
            message = f"Please provide a valid cuisine type. Supported cuisines are: {', '.join(supported_cuisines)}."
            if language == SIN:
                message = f"කරුණාකර නිවැරදි ආහාර වර්ගයක් ලබා දෙන්න. ආහාර වර්ග පහත ලැයිස්තුවෙන් ලබා දෙන්න: {', '.join(supported_cuisines)}."
            return False, message

    @staticmethod
    def validate_user_id(user_id: str, tracker: Tracker) -> Tuple[bool, str]:
        language = LanguageSelector.get_language(tracker)
        if user_id.startswith("uid"):
            return True, ""
        else:
            message = "User ID should start with 'uid'. Please provide a valid user ID."
            if language == SIN:
                message = "User ID සඳහා 'uid' ආරම්භ කිරීම අවශ්‍ය වේ. කරුණාකර නිවැරදි User ID ලබා දෙන්න."
            return False, message

    @staticmethod
    def validate_user_name(user_name: str, tracker: Tracker) -> Tuple[bool, str, str]:
        language = LanguageSelector.get_language(tracker)
        user_name = user_name.strip()
        if len(user_name) >= 3:
            return True, user_name, ""
        else:
            message = "Please provide a username with at least 3 characters."
            if language == SIN:
                message = "username සදහා අවම අකුරු 3ක් වත් අඩංගු විය යුතුයි."
            return False, "", message

    @staticmethod
    def validate_email(email: str, tracker: Tracker) -> Tuple[bool, str, str]:
        language = LanguageSelector.get_language(tracker)
        email = email.strip()
        if email:
            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if re.match(email_regex, email):
                # check if email is already registered
                user_repository = UserRepository()
                user = user_repository.find_user_by_email(email)
                if user:
                    message = "This email is already registered. Please provide a different email."
                    if language == SIN:
                        message = "මෙම email ලිපිනය දැනටමත් ලියාපදිංචි වී ඇත. කරුණාකර වෙනත් email ලිපිනයක් ලබා දෙන්න."
                    return False, "", message
                return True, email, ""
            else:
                message = "Please provide a valid email address."
                if language == SIN:
                    message = "කරුණාකර නිවැරදි email ලිපිනයක් ලබා දෙන්න."
                return False, "", message
        else:
            message = "Please provide a valid email address."
            if language == SIN:
                message = "කරුණාකර නිවැරදි email ලිපිනයක් ලබා දෙන්න."
            return False, "", message

    @staticmethod
    def validate_password(password: str, tracker: Tracker) -> Tuple[bool, str, str]:
        language = LanguageSelector.get_language(tracker)
        password = password.strip()
        if len(password) >= 4:
            return True, password, ""
        else:
            message = "Please provide a password with at least 4 characters."
            if language == SIN:
                message = "කරුණාකර අවම අකුරු 4ක් වත් අඩංගු password එකක් ඇතුලත් කරන්න."
            return False, "", message

    @staticmethod
    def validate_time(time: str, tracker: Tracker) -> Tuple[bool, str, str]:
        language = LanguageSelector.get_language(tracker)
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
                message = "Please provide a valid time in either 24-hour format (e.g., '14:30' or '06:15') or " \
                          "12-hour format (e.g., '2:30 PM' or '6:15 AM')."
                if language == SIN:
                    message = "කරුණාකර වලංගු කාලයක් පැය 24 ආකෘතියෙන් ලබා දෙන්න (උදා: '14:30' හෝ '06:15') හෝ " \
                              "පැය-12 ආකෘතිය (උදා: 'ප.ව. 2:30' හෝ 'පෙ.ව. 6:15')."
                return False, "", message

    @staticmethod
    def validate_booking_id(booking_reference_id: str, tracker: Tracker) -> Tuple[bool, str]:
        language = LanguageSelector.get_language(tracker)
        if booking_reference_id.startswith("bid_"):
            return True, ""
        else:
            message = "Please select a valid booking."
            if language == SIN:
                message = "කරුණාකර වලංගු වෙන් කිරීමක් තෝරන්න."
            return False, message
