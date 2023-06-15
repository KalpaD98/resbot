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
            language = LanguageSelector.get_language(tracker)

            if not booking:
                message = "No booking found with the provided ID."
                if language == SIN:
                    message = "ලබා දුන් ID සමග booking නොමැත."
                dispatcher.utter_message(text=message)
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
            language = LanguageSelector.get_language(tracker)

            if booking_id is None:
                logging.error("Booking ID not found")
                message = "Error occurred while fetching selected booking"
                if language == SIN:
                    message = "තෝරාගත් booking එක ලබා ගැනීමේදී දෝෂයක් සිදු වී ඇත"
                dispatcher.utter_message(text=message)
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
                    message = f"updated date to {new_date}"
                    if language == SIN:
                        message = f"දිනය {new_date}ට යාවත්කාලීන කර ඇත"
                    update_messages.append(message)
                if new_num_people:
                    message = f"updated number of people to {new_num_people}"
                    if language == SIN:
                        message = f"පුද්ගලයාගේ ගණන {new_num_people}ට යාවත්කාලීන කර ඇත"
                    update_messages.append(message)

                final_update_message = f"Your booking has been changed successfully {' and '.join(update_messages)}."

                if language == SIN:
                    final_update_message = f"ඔබගේ booking එක සාර්ථකව වෙනස් කර ඇත {' '.join(update_messages)}."
                dispatcher.utter_message(
                    text=final_update_message)

                return [SlotSet("date", None), SlotSet("num_people", None)]
            else:
                message = "No changes were made to your booking."
                if language == SIN:
                    message = "ඔබගේ booking එකට කිසිදු වෙනසක් සිදු කරේ නැත."
                dispatcher.utter_message(text=message)

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
        language = LanguageSelector.get_language(tracker)

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
        message = "What would you like to change?"

        if language == SIN:
            message = "ඔබ වෙනස් කිරීමට කැමති බලාපොරොත්තු වන්නෙ කුමක්ද?"
            options = [
                {
                    TITLE: "දිනය සහ පුද්ගලයාගේ ගණන",
                    PAYLOAD: "/user_wants_to_change_both_restaurant_booking_date_and_num_people",
                },
                {
                    TITLE: "දිනය පමනයි",
                    PAYLOAD: "/user_wants_to_change_restaurant_booking_date",
                },
                {
                    TITLE: "පුද්ගලයාගේ ගණන පමනයි",
                    PAYLOAD: "/user_wants_to_change_restaurant_booking_num_people",
                },
            ]

        quick_replies = ResponseGenerator.quick_replies(options, with_payload=True)
        dispatcher.utter_message(text=message, quick_replies=quick_replies)
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
            language = LanguageSelector.get_language(tracker)

            # Fetch the current booking details
            booking = booking_repo.find_booking_by_id(booking_id)
            if not booking:
                message = "No booking found with the provided ID."
                if language == SIN:
                    message = "ලබා දී ඇති ID හරහා කිසිදු booking එකක් නැත."
                dispatcher.utter_message(text=message)
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
                    restaurant=restaurant,
                    language=language
                )

                # Ask for user confirmation
                dispatcher.utter_message(text=comparison_text)
                message = "Do you want to confirm these changes?"
                if language == SIN:
                    message = "මෙම වෙනස්කම් තහවුරු කරන්නේද?"
                dispatcher.utter_message(
                    text=message,
                    quick_replies=ResponseGenerator.quick_reply_yes_no_with_payload(language=language)
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
