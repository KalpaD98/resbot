import datetime
from datetime import datetime
from typing import Tuple


class SlotValidator:
    @staticmethod
    def validate_date(date_entity: str) -> (bool, str, str):
        if date_entity:
            try:
                date_obj = datetime.strptime(date_entity, "%d-%m-%Y").date()
            except ValueError:
                return False, "", "I couldn't understand the date you provided. It seems to be invalid. Please try " \
                                  "again."

            today = datetime.now().date()
            tomorrow = today + datetime.timedelta(days=1)

            if date_obj >= tomorrow:
                return True, date_obj.isoformat(), ""
            else:
                return False, "", "Please provide a date that is tomorrow or later."
        else:
            return False, "", "I couldn't understand the date you provided. It seems to be invalid. Please try again."

    @staticmethod
    def validate_user_id(user_id: str) -> Tuple[bool, str]:
        if user_id.startswith("uid"):
            return True, ""
        else:
            return False, "User ID should start with 'uid'. Please provide a valid user ID."

    @staticmethod
    def validate_restaurant_id(restaurant_id: str) -> Tuple[bool, str]:
        if restaurant_id.startswith("rtid"):
            return True, ""
        else:
            return False, "Restaurant ID should start with 'rtid'. Please provide a valid restaurant ID."

    @staticmethod
    def validate_cuisine(cuisine: str) -> Tuple[bool, str]:
        supported_cuisines = ["Italian", "Chinese", "Indian", "Mexican", "Japanese"]
        if cuisine.lower() in [c.lower() for c in supported_cuisines]:
            return True, ""
        else:
            return False, f"Please provide a valid cuisine type. Supported cuisines are: {', '.join(supported_cuisines)}."

    @staticmethod
    def validate_num_people(num_people: str) -> Tuple[bool, str]:
        try:
            num = int(num_people)
            if num > 0:
                return True, ""
            else:
                return False, "The number of people should be greater than 0. Please provide a valid number."
        except ValueError:
            return False, "Please provide a valid number for the number of people."

    @staticmethod
    def validate_time(time: str) -> Tuple[bool, str, str]:
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
    def validate_booking_reference_id(booking_reference_id: str) -> Tuple[bool, str]:
        if booking_reference_id.startswith("brid"):
            return True, ""
        else:
            return False, "Please provide a valid booking reference ID (e.g., 'brid_1234')."
