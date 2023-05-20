# Actions.py This files contains custom all_actions which can be used to run custom Python code.
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from rasa_sdk.events import UserUtteranceReverted

# noinspection PyUnresolvedReferences
from actions.all_actions.bot_response_actions import *  # bot response actions
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
from actions.all_actions.restaurant_search_actions import *  # restaurant search actions
# noinspection PyUnresolvedReferences
from actions.all_actions.slot_validation_actions import *  # slot validation actions
# User related actions
# noinspection PyUnresolvedReferences
from actions.all_actions.user_actions import *  # user actions
# noinspection PyUnresolvedReferences
from actions.all_actions.user_preference_action import *  # user preference actions

# CONSTANTS
ACTION_ASK_ANYTHING_ELSE = "action_ask_anything_else"
ACTION_ASK_WHAT_USER_WANTS = "action_ask_what_user_wants"
ACTION_DEFAULT_FALLBACK_NAME = "action_default_fallback"
ACTION_CLEAR_RESTAURANT_BOOKING_SLOTS = "action_clear_restaurant_booking_slots"


class ActionDefaultFallback(Action):
    """Executes the fallback action and
    goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return ACTION_DEFAULT_FALLBACK_NAME

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        language = LanguageSelector.get_language(tracker)
        if language == SIN:
            dispatcher.utter_message(template="my_custom_fallback_template_sin")
        else:
            dispatcher.utter_message(template="my_custom_fallback_template")

        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]


class ActionAnythingElse(Action):
    def name(self) -> Text:
        return ACTION_ASK_ANYTHING_ELSE

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_text = "Is there anything else I can help you with?"
        sinhala_text = "ඔබට අවශ්යයි වෙනත් යමක් තිබේද?"

        english_quick_replies_with_payload = [
            {"title": QR_SEARCH_RESTAURANTS, "payload": "/want_to_search_restaurants"},
            {"title": QR_BROWSE_RESTAURANTS, "payload": "/request_restaurants"},
            {"title": "View bookings", "payload": "/view_bookings"},
            {"title": "No thanks", "payload": "/goodbye"},
        ]

        sinhala_quick_replies_with_payload = [
            {"title": "ආපනශාලා සොයන්න", "payload": "/want_to_search_restaurants"},
            {"title": "ආපනශාලා පෙන්වන්න", "payload": "/request_restaurants"},
            {"title": "Bookings පෙන්වන්න", "payload": "/view_bookings"},
            {"title": "නැත ස්තුතියි", "payload": "/goodbye"},
        ]

        final_text, final_quick_replies_with_payload = \
            ResponseGenerator.language_related_response_selection(
                tracker.get_slot(LANGUAGE),
                english_text,
                english_quick_replies_with_payload,
                sinhala_text,
                sinhala_quick_replies_with_payload)

        dispatcher.utter_message(text=final_text,
                                 quick_replies=ResponseGenerator.quick_replies(final_quick_replies_with_payload, True))
        return []


# anything else with quick replies
class ActionAskWhatUserWants(Action):
    def name(self) -> Text:
        return ACTION_ASK_WHAT_USER_WANTS

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_text = "What do you want to do?"
        sinhala_text = "ඔබට අවශ්ය සේවාව කුමක් ද?"

        english_quick_replies_with_payload = [
            {
                TITLE: QR_HI,
                PAYLOAD: "/greet"},
            {
                TITLE: QR_BROWSE_RESTAURANTS,
                PAYLOAD: "/request_restaurants"},
            {
                TITLE: QR_SEARCH_RESTAURANTS,
                PAYLOAD: "/want_to_search_restaurants"}
        ]

        sinhala_quick_replies_with_payload = [
            {
                TITLE: QR_HI,
                PAYLOAD: "/greet"},
            {
                TITLE: "ආපනශාලා පෙන්වන්න",
                PAYLOAD: "/request_restaurants"},
            {
                TITLE: "ආපනශාලා සොයන්න",
                PAYLOAD: "/want_to_search_restaurants"}
        ]

        final_text, final_quick_replies_with_payload = \
            ResponseGenerator.language_related_response_selection(
                tracker.get_slot(LANGUAGE),
                english_text,
                english_quick_replies_with_payload,
                sinhala_text,
                sinhala_quick_replies_with_payload)

        dispatcher.utter_message(text=final_text,
                                 quick_replies=ResponseGenerator.quick_replies(final_quick_replies_with_payload, True))
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
                SlotSet(BOOKING_ID, None),
                SlotSet(SELECTED_RESTAURANT, None),
                SlotSet(NUM_PEOPLE, None),
                SlotSet(DATE, None),
                SlotSet(TIME, None)]
