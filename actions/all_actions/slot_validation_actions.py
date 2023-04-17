from actions.all_actions.common_imports_for_actions import *

# CONSTANTS
ACTION_VALIDATE_DATE = "action_validate_date"
ACTION_VALIDATE_USER_ID = "action_validate_user_id"
ACTION_VALIDATE_RESTAURANT_ID = "action_validate_restaurant_id"
ACTION_VALIDATE_CUISINE = "action_validate_cuisine"
ACTION_VALIDATE_NUM_PEOPLE = "action_validate_num_people"
ACTION_VALIDATE_TIME = "action_validate_time"
ACTION_VALIDATE_BOOKING_ID = "action_validate_booking_id"


class ActionValidateRestaurantId(Action):
    def name(self) -> Text:
        return ACTION_VALIDATE_RESTAURANT_ID

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[EventType]:
        restaurant_id = tracker.get_slot(RESTAURANT_ID)
        is_valid, message = SlotValidators.validate_restaurant_id(restaurant_id)

        if is_valid:
            return [SlotSet(RESTAURANT_ID, restaurant_id)]
        else:
            dispatcher.utter_message(text=message)
            return [SlotSet(RESTAURANT_ID, None)]


class ActionValidateNumPeople(Action):
    def name(self) -> Text:
        return ACTION_VALIDATE_NUM_PEOPLE

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[EventType]:
        num_people = tracker.get_slot(NUM_PEOPLE)
        is_valid, message = SlotValidators.validate_num_people(num_people)

        if is_valid:
            return [SlotSet(NUM_PEOPLE, num_people)]
        else:
            dispatcher.utter_message(text=message)
            return [SlotSet(NUM_PEOPLE, None)]


class ActionAskDate(Action):
    def name(self) -> Text:
        return "action_ask_date"

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[EventType]:
        dispatcher.utter_message(text="Can you please provide the date again")
        dispatcher.utter_message(text="you can enter the date in a format like dd/mm/yyyy or similar")
        return []


class ActionValidateDate(Action):
    def name(self) -> Text:
        return "action_validate_date"

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[EventType]:
        date_slot = "date"
        date = tracker.get_slot(date_slot)
        is_valid, date_value, message = SlotValidators.validate_date(date)

        if is_valid:
            return [SlotSet(date_slot, date_value)]
        else:
            dispatcher.utter_message(text=message)
            return [SlotSet(date_slot, None), FollowupAction("action_ask_date")]


class DateForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_date_form"

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


class ActionValidateTime(Action):
    def name(self) -> Text:
        return ACTION_VALIDATE_TIME

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[EventType]:
        time = tracker.get_slot(TIME)
        is_valid, time_value, message = SlotValidators.validate_time(time)

        if is_valid:
            return [SlotSet(TIME, time_value)]
        else:
            dispatcher.utter_message(text=message)
            return [SlotSet(TIME, None)]


class ActionValidateUserId(Action):
    def name(self) -> Text:
        return ACTION_VALIDATE_USER_ID

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[EventType]:
        user_id = tracker.get_slot(USER_ID)
        is_valid, message = SlotValidators.validate_user_id(user_id)

        if is_valid:
            return [SlotSet(USER_ID, user_id)]
        else:
            dispatcher.utter_message(text=message)
            return [SlotSet(USER_ID, None)]


class ActionValidateCuisine(Action):
    def name(self) -> Text:
        return ACTION_VALIDATE_CUISINE

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[EventType]:
        cuisine = tracker.get_slot(CUISINE)
        is_valid, message = SlotValidators.validate_cuisine(cuisine)

        if is_valid:
            return [SlotSet(CUISINE, cuisine)]
        else:
            dispatcher.utter_message(text=message)
            return [SlotSet(CUISINE, None)]


class ActionValidateBookingReferenceId(Action):
    def name(self) -> Text:
        return ACTION_VALIDATE_BOOKING_ID

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        booking_reference_id = tracker.get_slot(BOOKING_ID)
        is_valid, message = SlotValidators.validate_booking_reference_id(booking_reference_id)

        if is_valid:
            return [SlotSet(BOOKING_ID, booking_reference_id)]
        else:
            dispatcher.utter_message(text=message)
            return [SlotSet(BOOKING_ID, None)]
