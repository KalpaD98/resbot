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
        quick_replies_with_payload = []

        quick_reply_view_all_bookings = {
            TITLE: "All Bookings",
            PAYLOAD: "/view_all_bookings"
        }

        quick_reply_view_past_bookings = {
            TITLE: "Past Bookings",
            PAYLOAD: "/view_past_bookings"
        }

        quick_reply_view_future_bookings = {
            TITLE: "Future Bookings",
            PAYLOAD: "/view_upcoming_bookings"
        }

        quick_replies_with_payload.append(quick_reply_view_all_bookings)
        quick_replies_with_payload.append(quick_reply_view_past_bookings)
        quick_replies_with_payload.append(quick_reply_view_future_bookings)

        dispatcher.utter_message(text="Choose what you want to see:",
                                 quick_replies=ResponseGenerator.quick_replies(quick_replies_with_payload, True))
        return []


class ActionShowBookingsCarousal(Action):

    def name(self) -> Text:
        return ACTION_SHOW_BOOKINGS_CAROUSAL

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # get list of user bookings from database sorted by date and filter by user_id
        user_id = tracker.get_slot(USER_ID)

        # TODO: handle this
        # if user_id is None:
        #     dispatcher.utter_message(response="utter_login_to_continue")
        #     return [FollowupAction(ACTION_LOGIN)]

        user_bookings = booking_repo.get_bookings_by_user_id(user_id)

        # Extract the list of unique restaurant IDs from the user bookings
        unique_restaurant_ids = list(set([booking["restaurant_id"] for booking in user_bookings]))

        # Fetch the corresponding restaurant data
        restaurant_data_dict = restaurant_repo.get_restaurants_by_ids(unique_restaurant_ids)

        # Prepare carousel items
        carousel_items = BookingResponseGenerator.booking_list_to_carousal_object(user_bookings, restaurant_data_dict)

        # Send carousel to the user using your custom response generator
        dispatcher.utter_message(
            attachment=ResponseGenerator.card_options_carousal(carousel_items)
        )

        return []


# actions.py

class ActionShowPastBookingsCarousal(ActionShowBookingsCarousal):
    def name(self) -> Text:
        return ACTION_SHOW_PAST_BOOKINGS_CAROUSAL

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_id = tracker.get_slot(USER_ID)
        user_bookings = booking_repo.get_past_bookings_by_user_id(user_id)

        unique_restaurant_ids = list(set([booking["restaurant_id"] for booking in user_bookings]))
        restaurant_data_dict = restaurant_repo.get_restaurants_by_ids(unique_restaurant_ids)
        carousel_items = BookingResponseGenerator.booking_list_to_carousal_object(user_bookings, restaurant_data_dict)

        dispatcher.utter_message(
            attachment=ResponseGenerator.card_options_carousal(carousel_items)
        )

        return []


class ActionShowFutureBookingsCarousal(ActionShowBookingsCarousal):
    def name(self) -> Text:
        return ACTION_SHOW_FUTURE_BOOKINGS_CAROUSAL

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_id = tracker.get_slot(USER_ID)
        user_bookings = booking_repo.get_future_bookings_by_user_id(user_id)

        unique_restaurant_ids = list(set([booking["restaurant_id"] for booking in user_bookings]))
        restaurant_data_dict = restaurant_repo.get_restaurants_by_ids(unique_restaurant_ids)
        carousel_items = BookingResponseGenerator.booking_list_to_carousal_object(user_bookings, restaurant_data_dict)

        dispatcher.utter_message(
            attachment=ResponseGenerator.card_options_carousal(carousel_items)
        )

        return []