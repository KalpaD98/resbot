# restaurant_booking_carousal_actions.py
from actions.all_actions.common_imports_for_actions import *
from actions.all_actions.helper_functions.response_generator.booking_response_generator import BookingResponseGenerator

ACTION_SHOW_BOOKINGS_CAROUSAL = "action_show_bookings_carousal"
ACTION_SHOW_FUTURE_BOOKINGS_CAROUSAL = "action_show_future_bookings_carousal"
ACTION_SHOW_PAST_BOOKINGS_CAROUSAL = "action_show_past_bookings_carousal"
ACTION_SHOW_BOOKING_VIEW_OPTIONS = "action_show_booking_view_options"


class ActionShowBookingOptions(Action):
    def name(self) -> Text:
        return ACTION_SHOW_BOOKING_VIEW_OPTIONS

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            language = LanguageSelector.get_language(tracker)

            quick_replies_with_payload = [{
                TITLE: "All bookings",
                PAYLOAD: "/view_all_bookings"
            }, {
                TITLE: "Upcoming bookings",
                PAYLOAD: "/view_upcoming_bookings"
            }, {
                TITLE: "Past bookings",
                PAYLOAD: "/view_past_bookings"
            }, ]

            message = "Choose which bookings you want to view"

            if language == SIN:
                message = "ඔබට බැලීමට අවශය bookings මොනවාද?"
                quick_replies_with_payload = [{
                    TITLE: "සියලුම bookings",
                    PAYLOAD: "/view_all_bookings"
                }, {
                    TITLE: "ඉදිරියෙදි එන bookings",
                    PAYLOAD: "/view_upcoming_bookings"
                }, {
                    TITLE: "පසුගිය bookings",
                    PAYLOAD: "/view_past_bookings"
                }, ]

            dispatcher.utter_message(text=message,
                                     quick_replies=ResponseGenerator.quick_replies(quick_replies_with_payload, True))
        except Exception as e:
            logger.error(f"An error occurred in ActionShowBookingOptions: {e}")
            dispatcher.utter_message(text="An error occurred. Please try again later.")

        return []


# Other action classes follow the same structure as above, adding a try-except block
# around the main code in the `run` method and logging errors.
class ActionShowBookingsCarousal(Action):

    def name(self) -> Text:
        return ACTION_SHOW_BOOKINGS_CAROUSAL

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:

            user_id = tracker.get_slot(USER_ID)
            user_bookings = booking_repo.get_bookings_by_user_id(user_id)
            language = LanguageSelector.get_language(tracker)

            if len(user_bookings) == 0:
                dispatcher.utter_message(text="Sorry, there are no bookings found for you.")
                return []

            unique_restaurant_ids = list(set([booking.restaurant_id for booking in user_bookings]))
            restaurant_data_dict = restaurant_repo.get_restaurants_by_ids(unique_restaurant_ids)
            carousel_items = BookingResponseGenerator.booking_list_to_carousal_object(user_bookings,
                                                                                      restaurant_data_dict)

            message = "Here's all your restaurant bookings"

            if LanguageSelector.get_language(tracker) == SIN:
                message = "ඔබේ වෙන් කිරීම් මෙන්න"

            dispatcher.utter_message(text=message)
            dispatcher.utter_message(attachment=ResponseGenerator.card_options_carousal(carousel_items))

        except Exception as e:
            logger.error(f"An error occurred in ActionShowBookingsCarousal: {e}")
            dispatcher.utter_message(text="An error occurred. Please try again later.")

        return []


# actions.py

class ActionShowPastBookingsCarousal(Action):
    def name(self) -> Text:
        return ACTION_SHOW_PAST_BOOKINGS_CAROUSAL

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            user_id = tracker.get_slot(USER_ID)
            user_bookings = booking_repo.get_past_bookings_by_user_id(user_id)
            language = LanguageSelector.get_language(tracker)

            if len(user_bookings) == 0:
                message = "Sorry, there are no past bookings found for you."
                if language == SIN:
                    message = "කණගාටුයි, ඔබට පසුගිය bookings නැත"
                dispatcher.utter_message(text=message)
                return []

            unique_restaurant_ids = list(set([booking.restaurant_id for booking in user_bookings]))
            restaurant_data_dict = restaurant_repo.get_restaurants_by_ids(unique_restaurant_ids)
            carousel_items = BookingResponseGenerator.booking_list_to_carousal_object(user_bookings,
                                                                                      restaurant_data_dict)
            message = "Here's all your past restaurant bookings"
            if language == SIN:
                message = "ඔබගේ පසුගිය bookings මෙන්න"

            dispatcher.utter_message(text=message,attachment=ResponseGenerator.card_options_carousal(carousel_items))

        except Exception as e:
            logger.error(f"An error occurred in ActionShowPastBookingsCarousal: {e}")
            dispatcher.utter_message(text="An error occurred. Please try again later.")

        return []


class ActionShowFutureBookingsCarousal(Action):
    def name(self) -> Text:
        return ACTION_SHOW_FUTURE_BOOKINGS_CAROUSAL

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            user_id = tracker.get_slot(USER_ID)
            user_bookings = booking_repo.get_future_bookings_by_user_id(user_id)
            language = LanguageSelector.get_language(tracker)

            if len(user_bookings) == 0:
                message = "Sorry, there are no upcoming bookings found for you."
                if language == SIN:
                    message = "ඔබට ඉදිරියෙදි එන bookings නැත"
                dispatcher.utter_message(text=message)
                return []

            unique_restaurant_ids = list(set([booking.restaurant_id for booking in user_bookings]))
            restaurant_data_dict = restaurant_repo.get_restaurants_by_ids(unique_restaurant_ids)
            carousel_items = BookingResponseGenerator.booking_list_to_carousal_object(user_bookings,
                                                                                      restaurant_data_dict)

            dispatcher.utter_message(attachment=ResponseGenerator.card_options_carousal(carousel_items))

        except Exception as e:
            logger.error(f"An error occurred in ActionShowFutureBookingsCarousal: {e}")
            dispatcher.utter_message(text="An error occurred. Please try again later.")

        return []
