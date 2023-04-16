from actions.all_actions.common_imports_for_actions import *

ACTION_CHANGE_RESTAURANT_BOOKING_DATE = "action_change_restaurant_booking_date"
ACTION_SHOW_NEW_BOOKING_DETAILS = "action_show_new_booking_details"


class ActionChangeBookingDate(Action):
    def name(self) -> Text:
        return ACTION_CHANGE_RESTAURANT_BOOKING_DATE

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            booking_id = tracker.get_slot(BOOKING_ID)
            new_date = tracker.get_slot(DATE)

            # Update the booking date in system here.
            # call  API to update database.

            # Send a confirmation message to the user
            dispatcher.utter_message(
                text=f"Your booking with ID {booking_id} has been successfully updated to {new_date}.")
            return [SlotSet("date", None)]
        except Exception as e:
            logger.error(f"An error occurred in ActionChangeBookingDate: {e}")
            dispatcher.utter_message(text="An error occurred. Please try again later.")

        return []


class ActionShowNewBookingDetails(Action):

    def name(self) -> Text:
        return ACTION_SHOW_NEW_BOOKING_DETAILS

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            booking_id = tracker.get_slot("booking_id")
            date = tracker.get_slot("date")

            # Mock booking details
            booking_details = {
                'booking_id': 'bid_123',
                'restaurant_name': 'The Fancy Restaurant',
                'date': '2023-03-30',
                # 'time': '19:00',
                'num_people': 4
            }

            if booking_details is not None:
                # Update the booking date in the booking_details
                booking_details['date'] = date

                # Format the message to show the updated booking details
                message = f"Here are the updated booking details:\n\n"
                message += f"Booking ID: {booking_details['booking_id']}\n"
                message += f"Restaurant: {booking_details['restaurant_name']}\n"
                message += f"Date: {booking_details['date']}\n"
                # message += f"Time: {booking_details['time']}\n"
                message += f"Number of people: {booking_details['num_people']}\n"

                dispatcher.utter_message(text=message)
                dispatcher.utter_message(text="would you like to confirm the change?")
                dispatcher.utter_message(quickreplies=ResponseGenerator.quick_reply_yes_no_with_payload())
            else:
                dispatcher.utter_message(text="Sorry, I couldn't find the booking details.")

        except Exception as e:
            logger.error(f"An error occurred in ActionShowNewBookingDetails: {e}")
            dispatcher.utter_message(text="An error occurred. Please try again later.")

        return []
