from actions.all_actions.common_imports_for_actions import *
from actions.all_actions.helper_functions.response_generator.booking_response_generator import BookingResponseGenerator

ACTION_CHANGE_RESTAURANT_BOOKING_DETAILS = "action_change_restaurant_booking_details"
ACTION_SHOW_NEW_BOOKING_DETAILS = "action_show_new_booking_details"
ACTION_SHOW_SELECTED_BOOKING_DETAILS = "action_show_selected_booking_details"
ACTION_ASK_WHAT_USER_WANT_TO_CHANGE_IN_BOOKING = "action_ask_what_user_want_to_change_in_booking"
ACTION_VALIDATE_AND_COMPARE_BOOKING_CHANGES_ASK_CONFIRMATION_TO_CHANGE \
    = "action_validate_and_compare_booking_changes_ask_confirmation_to_change"
ACTION_CLEAR_BOOKING_DATA_SLOTS = "action_clear_booking_data_slots"


class ActionShowCurrentBookingDetails(Action):
    def name(self) -> Text:
        return ACTION_SHOW_SELECTED_BOOKING_DETAILS

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            booking_id = tracker.get_slot(BOOKING_ID)
            booking = booking_repo.find_booking_by_id(booking_id)

            if not booking:
                dispatcher.utter_message(text="No booking found with the provided ID.")
                return []

            restaurant = restaurant_repo.find_restaurant_by_id(booking.restaurant_id)
            booking_details_text = BookingResponseGenerator.generate_booking_details_text(booking, restaurant)

            dispatcher.utter_message(text=booking_details_text)

        except Exception as e:
            logger.error(f"An error occurred in ActionShowCurrentBookingDetails: {e}")
            dispatcher.utter_message(text="An error occurred. Please try again later.")

        return []


class ActionChangeBookingDetails(Action):
    def name(self) -> Text:
        return ACTION_CHANGE_RESTAURANT_BOOKING_DETAILS

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            booking_id = tracker.get_slot(BOOKING_ID)
            new_date = tracker.get_slot(DATE)
            new_num_people = tracker.get_slot(NUM_PEOPLE)
            if booking_id is None:
                logging.error("Booking ID not found")
                dispatcher.utter_message(text="Error occurred while fetching selected booking")
                return [FollowupAction("action_show_future_bookings_carousal")]
            # Update the booking date and/or number of people in the system here.
            booking_updates = {}
            if new_date:
                booking_updates["date"] = new_date
            if new_num_people:
                booking_updates["num_people"] = new_num_people

            if booking_updates:
                booking_repo.modify_booking(booking_id, **booking_updates)

                # Send a confirmation message to the user
                update_messages = []
                if new_date:
                    update_messages.append(f"updated date to {new_date}")
                if new_num_people:
                    update_messages.append(f"updated number of people to {new_num_people}")

                dispatcher.utter_message(
                    text=f"Your booking has been changed successfully {' and '.join(update_messages)}.")

                return [SlotSet("date", None), SlotSet("num_people", None)]
            else:
                dispatcher.utter_message(text="No changes were made to your booking.")

        except Exception as e:
            logger.error(f"An error occurred in ActionChangeBookingDetails: {e}")
            dispatcher.utter_message(text="An error occurred. Please try again later.")

        return []


class ActionAskWhatUserWantToChangeInBooking(Action):
    def name(self) -> Text:
        return ACTION_ASK_WHAT_USER_WANT_TO_CHANGE_IN_BOOKING

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[EventType]:
        options = [
            {
                TITLE: "Date and Number of People",
                PAYLOAD: "/user_wants_to_change_both_restaurant_booking_date_and_num_people",
            },
            {
                TITLE: "Date",
                PAYLOAD: "/user_wants_to_change_restaurant_booking_date",
            },
            {
                TITLE: "Number of people",
                PAYLOAD: "/user_wants_to_change_restaurant_booking_num_people",
            },
        ]

        quick_replies = ResponseGenerator.quick_replies(options, with_payload=True)
        dispatcher.utter_message(text="What would you like to change?", quick_replies=quick_replies)
        return []


class ActionValidateAndCompareBookingChanges(Action):
    def name(self) -> Text:
        return ACTION_VALIDATE_AND_COMPARE_BOOKING_CHANGES_ASK_CONFIRMATION_TO_CHANGE

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            booking_id = tracker.get_slot(BOOKING_ID)
            new_date = tracker.get_slot(DATE)
            new_num_people = tracker.get_slot(NUM_PEOPLE)

            # Fetch the current booking details
            booking = booking_repo.find_booking_by_id(booking_id)
            if not booking:
                dispatcher.utter_message(text="No booking found with the provided ID.")
                return [FollowupAction("action_show_future_bookings_carousal")]

            restaurant = restaurant_repo.find_restaurant_by_id(booking.restaurant_id)

            # Check if any changes were made
            has_changes = False
            if (new_date and new_date != booking.date) or (new_num_people and new_num_people != booking.num_people):
                has_changes = True

            if has_changes:
                # Create a new booking object with the updated information
                updated_booking = booking.copy()
                updated_booking.date = new_date if new_date else booking.date
                updated_booking.num_people = new_num_people if new_num_people else booking.num_people

                # Compare old and new booking details and generate text
                comparison_text = BookingResponseGenerator.generate_booking_comparison_text(
                    old_booking=booking,
                    new_booking=updated_booking,
                    restaurant=restaurant
                )

                # Ask for user confirmation
                dispatcher.utter_message(text=comparison_text)
                dispatcher.utter_message(
                    text="Do you want to confirm these changes?",
                    quick_replies=ResponseGenerator.quick_reply_yes_no_with_payload()
                )

        except Exception as e:
            logger.error(f"An error occurred in ActionValidateAndCompareBookingChanges: {e}")
            dispatcher.utter_message(text="An error occurred. Please try again later.")

        return []


class ActionClearBookingDataSlots(Action):
    def name(self) -> Text:
        return ACTION_CLEAR_BOOKING_DATA_SLOTS

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet(DATE, None), SlotSet(NUM_PEOPLE, None)]
