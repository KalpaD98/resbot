from actions.all_actions.common_imports_for_actions import *

ACTION_CANCEL_BOOKING = "action_cancel_booking"
ACTION_ASK_CANCEL_BOOKING_CONFIRMATION = "action_ask_cancel_booking_confirmation"


class ActionAskCancelBookingConfirmation(Action):
    def name(self) -> Text:
        return ACTION_ASK_CANCEL_BOOKING_CONFIRMATION

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cancel_booking_id = tracker.get_slot("cancel_booking_id")

        # Fetch booking information from the database using cancel_booking_id (customize this part)
        booking = {
            "booking_id": "bid_123",
            "restaurant_name": "Restaurant A",
            "booking_date": "2023-06-10",
            "num_people": 4
        }

        # change formatting of below message
        message = f"Are you sure you want to cancel the booking for {booking['restaurant_name']} on " \
                  f"{booking['booking_date']} for {booking['num_people']} people? This action cannot be undone."

        dispatcher.utter_message(text=message)

        return []


class ActionCancelBooking(Action):
    def name(self) -> Text:
        return ACTION_CANCEL_BOOKING

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[EventType]:
        cancel_booking_id = tracker.get_slot("cancel_booking_id")

        # Fetch booking information from the database using cancel_booking_id (customize this part)
        booking = {
            "booking_id": "bid_123",
            "restaurant_name": "Restaurant A",
            "booking_date": "2023-06-10",
            "num_people": 4
        }

        # Cancel the booking in the database using cancel_booking_id (customize this part)
        # Add a comment to indicate where the database operation should be done
        # For example: Cancel booking in the database using cancel_booking_id

        message = f"Your booking at {booking['restaurant_name']} on {booking['booking_date']} for {booking['num_people']} people has been successfully canceled."

        # Clear the cancel_booking_id slot
        return [SlotSet("cancel_booking_id", None), dispatcher.utter_message(text=message)]
