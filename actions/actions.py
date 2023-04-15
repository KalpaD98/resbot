# Actions.py This files contains custom all_actions which can be used to run custom Python code.
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

# ------ All other actions ------
# noinspection PyUnresolvedReferences
from actions.all_actions.form_validation_actions import *  # form validation actions
# noinspection PyUnresolvedReferences
from actions.all_actions.knowledge_base_actions import *  # knowledge base actions
# noinspection PyUnresolvedReferences
from actions.all_actions.restaurant_actions import *  # restaurant actions
# noinspection PyUnresolvedReferences
from actions.all_actions.restaurant_booking_actions import *  # restaurant booking actions
# noinspection PyUnresolvedReferences
from actions.all_actions.restaurant_booking_cancel_actions import *  # restaurant booking delete
# noinspection PyUnresolvedReferences
from actions.all_actions.restaurant_booking_carousal_actions import *  # restaurant booking read
# noinspection PyUnresolvedReferences
from actions.all_actions.restaurant_booking_change_actions import *  # restaurant booking update
# noinspection PyUnresolvedReferences
from actions.all_actions.slot_validation_actions import *  # slot validation actions
# noinspection PyUnresolvedReferences
from actions.all_actions.user_actions import *  # user actions

# CONSTANTS
ACTION_ASK_ANYTHING_ELSE = "action_ask_anything_else"
ACTION_ASK_WHAT_USER_WANTS = "action_ask_what_user_wants"
ACTION_DEFAULT_FALLBACK_NAME = "action_default_fallback"
ACTION_CLEAR_RESTAURANT_BOOKING_SLOTS = "action_clear_restaurant_booking_slots"


# anything else with quick replies
class ActionAnythingElse(Action):
    def name(self) -> Text:
        return ACTION_ASK_ANYTHING_ELSE

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # quick replies for show more and search with payload
        quick_replies_with_payload = []

        quick_reply_show_more = {
            TITLE: QR_SHOW_MORE_RESTAURANTS,
            PAYLOAD: "/request_more_restaurant_options"}

        quick_reply_no = {
            TITLE: "No thanks",
            PAYLOAD: "/goodbye"}

        quick_reply_search_restaurant = {
            TITLE: QR_SEARCH_RESTAURANTS,
            PAYLOAD: "/want_to_search_restaurants"}

        quick_replies_with_payload.append(quick_reply_show_more)
        quick_replies_with_payload.append(quick_reply_search_restaurant)
        quick_replies_with_payload.append(quick_reply_no)

        dispatcher.utter_message(text="Is there anything else I can help you with?",
                                 quick_replies=ResponseGenerator.quick_replies(quick_replies_with_payload, True))
        return []


# anything else with quick replies
class ActionAskWhatUserWants(Action):
    def name(self) -> Text:
        return ACTION_ASK_WHAT_USER_WANTS

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # quick replies for show more and search with payload
        quick_replies_with_payload = []

        quick_reply_say_hi = {
            TITLE: "Hi",
            PAYLOAD: "/greet"}

        quick_reply_request_restaurants = {
            TITLE: QR_SHOW_MORE_RESTAURANTS,
            PAYLOAD: "/request_restaurants"}

        quick_reply_search_restaurant = {
            TITLE: QR_SEARCH_RESTAURANTS,
            PAYLOAD: "/want_to_search_restaurants"}

        quick_replies_with_payload.append(quick_reply_say_hi)
        quick_replies_with_payload.append(quick_reply_request_restaurants)
        quick_replies_with_payload.append(quick_reply_search_restaurant)

        dispatcher.utter_message(text="What do you want to do?",
                                 quick_replies=ResponseGenerator.quick_replies(quick_replies_with_payload, True))
        return []


# clear slots related to restaurant booking when user ask to stop booking
class ActionClearRestaurantBookingSlots(Action):
    def name(self) -> Text:
        return ACTION_CLEAR_RESTAURANT_BOOKING_SLOTS

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet(CUISINE, None),
                SlotSet(RESTAURANT_ID, None),
                SlotSet(SELECTED_RESTAURANT, None),
                SlotSet(NUM_PEOPLE, None),
                SlotSet(DATE, None),
                SlotSet(TIME, None)]
