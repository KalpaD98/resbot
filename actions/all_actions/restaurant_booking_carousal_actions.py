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
            quick_replies_with_payload = []

            quick_reply_view_all_bookings = {
                TITLE: "All Bookings",
                PAYLOAD: "/view_all_bookings"
            }

            quick_reply_view_upcomming_bookings = {
                TITLE: "Upcoming Bookings",
                PAYLOAD: "/view_upcoming_bookings"
            }

            quick_reply_view_past_bookings = {
                TITLE: "Past Bookings",
                PAYLOAD: "/view_past_bookings"
            }

            quick_replies_with_payload.append(quick_reply_view_all_bookings)
            quick_replies_with_payload.append(quick_reply_view_upcomming_bookings)
            quick_replies_with_payload.append(quick_reply_view_past_bookings)

            dispatcher.utter_message(text="Choose which bookings you want to view",
                                     quick_replies=ResponseGenerator.quick_replies(quick_replies_with_payload, True))
        except Exception as e:
            logger.error(f"An error occurred in action_show_booking_options: {e}")
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

            if len(user_bookings) == 0:
                dispatcher.utter_message(response="utter_no_bookings_found")
                return []

            unique_restaurant_ids = list(set([booking.restaurant_id for booking in user_bookings]))
            restaurant_data_dict = restaurant_repo.get_restaurants_by_ids(unique_restaurant_ids)
            carousel_items = BookingResponseGenerator.booking_list_to_carousal_object(user_bookings,
                                                                                      restaurant_data_dict)

            dispatcher.utter_message(attachment=ResponseGenerator.card_options_carousal(carousel_items))

        except Exception as e:
            logger.error(f"An error occurred in action_show_bookings_carousal: {e}")
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

            if len(user_bookings) == 0:
                dispatcher.utter_message(response="utter_no_past_bookings_found")
                return []

            unique_restaurant_ids = list(set([booking.restaurant_id for booking in user_bookings]))
            restaurant_data_dict = restaurant_repo.get_restaurants_by_ids(unique_restaurant_ids)
            carousel_items = BookingResponseGenerator.booking_list_to_carousal_object(user_bookings,
                                                                                      restaurant_data_dict)

            dispatcher.utter_message(attachment=ResponseGenerator.card_options_carousal(carousel_items))

        except Exception as e:
            logger.error(f"An error occurred in action_show_booking_options: {e}")
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

            if len(user_bookings) == 0:
                dispatcher.utter_message(response="utter_no_future_bookings_found")
                return []

            unique_restaurant_ids = list(set([booking.restaurant_id for booking in user_bookings]))
            restaurant_data_dict = restaurant_repo.get_restaurants_by_ids(unique_restaurant_ids)
            carousel_items = BookingResponseGenerator.booking_list_to_carousal_object(user_bookings,
                                                                                      restaurant_data_dict)

            dispatcher.utter_message(attachment=ResponseGenerator.card_options_carousal(carousel_items))

        except Exception as e:
            logger.error(f"An error occurred in action_show_booking_options: {e}")
            dispatcher.utter_message(text="An error occurred. Please try again later.")

        return []
