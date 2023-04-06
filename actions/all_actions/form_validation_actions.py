from actions.all_actions.common_imports import *

VALIDATE_RESTAURANT_BOOKING_FORM = "validate_restaurant_booking_form"
VALIDATE_REGISTRATION_FORM = "validate_registration_form"
VALIDATE_LOGIN_FORM = "validate_login_form"
VALIDATE_CHANGE_RESTAURANT_BOOKING_DATE_FORM = "validate_change_restaurant_booking_date_form"


# VALIDATE_RESTAURANT_SEARCH_FORM = "validate_restaurant_search_form"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# --------------------------------------------- Form Validation Actions --------------------------------------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class ValidateRegistrationForm(FormValidationAction):
    def name(self) -> Text:
        return VALIDATE_REGISTRATION_FORM

    async def validate_name(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, name_value, message = SlotValidators.validate_user_name(value)
        if is_valid:
            return {"name": name_value}
        else:
            dispatcher.utter_message(text=message)
            return {"name": None}

    async def validate_email(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, email_value, message = SlotValidators.validate_email(value)
        if is_valid:
            return {"email": email_value}
        else:
            dispatcher.utter_message(text=message)
            return {"email": None}

    async def validate_password(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, password_value, message = SlotValidators.validate_password(value)
        if is_valid:
            return {"password": password_value}
        else:
            dispatcher.utter_message(text=message)
            return {"password": None}


class ValidateLoginForm(FormValidationAction):
    def name(self) -> Text:
        return VALIDATE_LOGIN_FORM

    async def validate_user_email(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, email, error_message = SlotValidators.validate_email(slot_value)
        if is_valid:
            return {"user_email": email}
        else:
            dispatcher.utter_message(text=error_message)
            return {"user_email": None}

    async def validate_user_password(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, password, error_message = SlotValidators.validate_password(slot_value)
        if is_valid:
            return {"user_password": password}
        else:
            dispatcher.utter_message(text=error_message)
            return {"user_password": None}


class RestaurantBookingForm(FormValidationAction):
    def name(self) -> Text:
        return VALIDATE_RESTAURANT_BOOKING_FORM

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Text]:
        return ["num_people", "date"]

    async def validate_num_people(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, message = SlotValidators.validate_num_people(value)
        if is_valid:
            return {"num_people": value}
        else:
            dispatcher.utter_message(text=message)
            return {"num_people": None}

    async def validate_date(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, date_value, message = SlotValidators.validate_date(value)
        if is_valid:
            return {"date": date_value}
        else:
            dispatcher.utter_message(text=message)
            return {"date": None}


class ChangeRestaurantBookingDateForm(FormValidationAction):
    def name(self) -> Text:
        return VALIDATE_CHANGE_RESTAURANT_BOOKING_DATE_FORM

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["date"]

    def validate_date(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            Dict[Text, Any]:
        is_valid, new_date, error_message = SlotValidators.validate_date(value)
        if not is_valid:
            dispatcher.utter_message(text=error_message)
            return {"date": None}
        else:
            return {"date": new_date}


# Add a function to find a user by email
def find_user_by_email(email: str) -> Optional[User]:
    # Implement the logic to find a user by email
    # You can use your MongoDB database to search for the user
    pass