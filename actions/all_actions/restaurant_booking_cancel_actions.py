from actions.all_actions.common_imports_for_actions import *

ACTION_CANCEL_BOOKING = "action_cancel_booking"
ACTION_ASK_CANCEL_BOOKING_CONFIRMATION = "action_ask_cancel_booking_confirmation"


class ActionAskCancelBookingConfirmation(Action):
    def name(self) -> Text:
        return ACTION_ASK_CANCEL_BOOKING_CONFIRMATION

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the booking_id from the slot
        booking_id = tracker.get_slot("booking_id")

        # Fetch booking information from the database using booking_id (customize this part)
        booking = booking_repo.find_booking_by_id(booking_id)

        restaurant = restaurant_repo.find_restaurant_by_id(booking.restaurant_id)

        message = f"Are you sure you want to cancel the booking for {restaurant.name} on " \
                  f"{booking.date} for {booking.num_people} people? This action cannot be undone."

        dispatcher.utter_message(text=message, quick_replies=ResponseGenerator.quick_reply_yes_no_with_payload())

        return []
class ActionCancelBooking(Action):
    def name(self) -> Text:
        return ACTION_CANCEL_BOOKING

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[EventType]:
        booking_id = tracker.get_slot("booking_id")

        # Fetch booking information from the database using booking_id (customize this part)
        booking = booking_repo.find_booking_by_id(booking_id)
        restaurant = restaurant_repo.find_restaurant_by_id(booking.restaurant_id)

        # Cancel the booking in the database using booking_id (customize this part)
        booking_repo.cancel_booking(booking_id)

        message = f"Your booking at {restaurant.name} on {booking.date} for {booking.num_people} people has been successfully canceled."

        # Clear the booking_id slot
        return [SlotSet("booking_id", None), dispatcher.utter_message(text=message)]
