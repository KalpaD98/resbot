from rasa_sdk.events import ActiveLoop

from actions.all_actions.common_imports_for_actions import *

VALIDATE_RESTAURANT_BOOKING_FORM = "validate_restaurant_booking_form"
VALIDATE_REGISTRATION_FORM = "validate_registration_form"
VALIDATE_LOGIN_FORM = "validate_login_form"
ACTION_DEACTIVATE_FORM = "action_deactivate_form"
VALIDATE_CHANGE_RESTAURANT_BOOKING_FORM = "validate_change_restaurant_booking_form"
VALIDATE_CHANGE_RESTAURANT_BOOKING_DATE_FORM = "validate_change_restaurant_booking_date_form"
VALIDATE_CHANGE_RESTAURANT_BOOKING_NUM_PEOPLE_FORM = "validate_change_restaurant_booking_num_people_form"


# VALIDATE_RESTAURANT_SEARCH_FORM = "validate_restaurant_search_form"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# --------------------------------------------- Form Validation Actions --------------------------------------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# ------------------------------------------------ User Related Forms ------------------------------------------------ #
class ValidateRegistrationForm(FormValidationAction):
    def name(self) -> Text:
        return VALIDATE_REGISTRATION_FORM

    async def validate_user_name(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, name_value, message = SlotValidators.validate_user_name(value, tracker)
        if is_valid:
            return {"user_name": name_value.capitalize()}
        else:
            dispatcher.utter_message(text=message)
            return {"user_name": None}

    async def validate_email(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, email_value, message = SlotValidators.validate_email(value, tracker)
        if is_valid:
            return {"user_email": email_value}
        else:
            dispatcher.utter_message(text=message)
            return {"user_email": None}

    async def validate_password(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, password_value, message = SlotValidators.validate_password(value, tracker)
        if is_valid:
            return {"user_password": password_value}
        else:
            dispatcher.utter_message(text=message)
            return {"user_password": None}


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
        is_valid, email, error_message = SlotValidators.validate_email(slot_value, tracker)
        user_exists = False
        # check if user exists with given mail

        if is_valid:
            # check there is a user with this email. if yes then return the email.
            user_exists = user_repo.find_user_by_email(email) is not None
            # if no utter no user registered then utter register -> followup with registration form
            if not user_exists:
                language = LanguageSelector.get_language(tracker)
                message = "No user registered with this email. Please register first."

                if language == SIN:
                    message = "මෙම email එකට අයත් පරිශීලකයෙක් නොමැත. කරුණාකර ලියාපදිංචි වන්න."

                dispatcher.utter_message(text=message)
                return {"user_email": None}

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
        is_valid, password, error_message = SlotValidators.validate_password(slot_value, tracker)
        if is_valid:
            # check if the password is correct for the user with the given email
            email = tracker.get_slot("user_email")
            user = user_repo.find_user_by_email(email)
            if user is not None:
                if user.password != password:
                    language = LanguageSelector.get_language(tracker)
                    message = "Incorrect password. Please try again."

                    if language == SIN:
                        message = "අවලංගු මුරපදයකි. නැවත උත්සාහ කරන්න."
                    dispatcher.utter_message(text=message)
                    return {"user_password": None}

            return {"logged_user": user}
        else:
            dispatcher.utter_message(text=error_message)
            return {"user_password": None}


########################################################################################################################

# --------------------------------------------- Restaurant Booking Forms --------------------------------------------- #

########################################################################################################################
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
        return ["restaurant_id", "user_id", "num_people", "date"]

    # Add validation methods for the new slots: restaurant_id and user_id
    # You can use the existing validation methods from the SlotValidators class

    async def validate_restaurant_id(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, message = SlotValidators.validate_restaurant_id(value, tracker)
        if is_valid:
            return {"restaurant_id": value}
        else:
            dispatcher.utter_message(text=message)
            return {"restaurant_id": None}

    async def validate_user_id(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, message = SlotValidators.validate_user_id(value, tracker)
        if is_valid:
            return {"user_id": value}
        else:
            dispatcher.utter_message(text=message)
            return {"user_id": None}

    # Use the existing validation methods for num_people and date slots

    async def validate_num_people(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, message = SlotValidators.validate_num_people(value, tracker)
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
        is_valid, date_value, message = SlotValidators.validate_date(value, tracker)
        if is_valid:
            return {"date": date_value}
        else:
            dispatcher.utter_message(text=message)
            return {"date": None}


class ChangeRestaurantBookingFormValidation(FormValidationAction):
    def name(self) -> Text:
        return VALIDATE_CHANGE_RESTAURANT_BOOKING_FORM

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Text]:
        return ["booking_id", "user_id", "date", "num_people"]

    # Add the validation methods for the new slots: booking_id and user_id
    # You can use the existing validation methods from the SlotValidators class

    async def validate_booking_id(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, message = SlotValidators.validate_booking_id(value, tracker)
        if is_valid:
            return {"booking_id": value}
        else:
            dispatcher.utter_message(text=message)
            return {"booking_id": None}

    async def validate_user_id(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, message = SlotValidators.validate_user_id(value, tracker)
        if is_valid:
            return {"user_id": value}
        else:
            dispatcher.utter_message(text=message)
            return {"user_id": None}

    # Use the existing validation methods for num_people and date slots

    async def validate_num_people(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, message = SlotValidators.validate_num_people(value, tracker)
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
        is_valid, date_value, message = SlotValidators.validate_date(value, tracker)
        if is_valid:
            return {"date": date_value}
        else:
            dispatcher.utter_message(text=message)
            return {"date": None}


class ChangeRestaurantBookingDateForm(FormValidationAction):
    def name(self) -> Text:
        return VALIDATE_CHANGE_RESTAURANT_BOOKING_DATE_FORM

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Text]:
        return ["date"]

    async def validate_date(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, date_value, message = SlotValidators.validate_date(value, tracker)
        if is_valid:
            return {"date": date_value}
        else:
            dispatcher.utter_message(text=message)
            return {"date": None}


class ChangeRestaurantBookingNumPeopleForm(FormValidationAction):
    def name(self) -> Text:
        return VALIDATE_CHANGE_RESTAURANT_BOOKING_NUM_PEOPLE_FORM

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Text]:
        return ["num_people"]

    async def validate_num_people(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, message = SlotValidators.validate_num_people(value, tracker)
        if is_valid:
            return {"num_people": value}
        else:
            dispatcher.utter_message(text=message)
            return {"num_people": None}


class ActionDeactivateForm(Action):
    def name(self) -> Text:
        return "action_deactivate_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [ActiveLoop(None), SlotSet("requested_slot", None)]
