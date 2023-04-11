from actions.all_actions.common_imports_for_actions import *

ACTION_SHOW_USER_BOOKINGS = "action_show_user_bookings"
ACTION_SHOW_PAST_BOOKINGS = "action_show_past_bookings"
ACTION_SHOW_UPCOMING_BOOKINGS = "action_show_upcoming_bookings"
ACTION_CHANGE_RESTAURANT_BOOKING_DATE = "action_change_restaurant_booking_date"
ACTION_SHOW_NEW_BOOKING_DETAILS = "action_show_new_booking_details"
ACTION_CANCEL_BOOKING = "action_cancel_booking"
ACTION_ASK_CANCEL_BOOKING_CONFIRMATION = "action_ask_cancel_booking_confirmation"


class ActionShowUserBookings(Action):
    def name(self) -> Text:
        return ACTION_SHOW_USER_BOOKINGS

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any],
                  booking_type: str) -> List[Dict[Text, Any]]:

        # can use slot user instead of user_id
        user_id = tracker.get_slot("user_id")
        # TODO: get user bookings from database
        user_bookings = ["get_user_bookings(user_id, booking_type)"]

        # check if bookings exist

        # if no bookings exist
        if len(user_bookings) == 0:
            dispatcher.utter_message(text="You have no bookings")
            return []

        # Prepare carousel items / TODO: refactor this to booking response generator
        carousel_items = []
        for booking in user_bookings:
            carousel_item = {
                "title": booking["restaurant_name"],
                "subtitle": f"Booking Date: {booking['booking_date']}",
                "image_url": booking["restaurant_image"],
                "buttons": [
                    {
                        "title": "Cancel Booking",
                        "type": "postback",
                        "payload": f"/inform_cancel_booking_id{{\"cancel_booking_id\": \"{booking['booking_id']}\"}}"
                    },
                    {
                        "title": "Change Date",
                        "type": "postback",
                        "payload": f"/inform_change_date_booking_id{{\"change_booking_date_id\": \"{booking['booking_id']}\"}}"
                    }
                ]
            }
            carousel_items.append(carousel_item)

        # Send carousel to the user using your custom response generator
        dispatcher.utter_message(
            attachment=ResponseGenerator.card_options_carousal(carousel_items)
        )

        return []


class ActionShowPastBookings(ActionShowUserBookings):
    def name(self) -> Text:
        return ACTION_SHOW_PAST_BOOKINGS

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return await super().run(dispatcher, tracker, domain, booking_type="past")


class ActionShowUpcomingBookings(ActionShowUserBookings):
    def name(self) -> Text:
        return ACTION_CHANGE_RESTAURANT_BOOKING_DATE

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return await super().run(dispatcher, tracker, domain, booking_type="upcoming")


class ActionChangeBookingDate(Action):
    def name(self) -> Text:
        return ACTION_CHANGE_RESTAURANT_BOOKING_DATE

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        booking_id = tracker.get_slot("booking_id")
        new_date = tracker.get_slot("date")

        # Update the booking date in system here.
        # call  API to update database.

        # Send a confirmation message to the user
        dispatcher.utter_message(text=f"Your booking with ID {booking_id} has been successfully updated to {new_date}.")
        return [SlotSet("date", None)]


class ActionShowNewBookingDetails(Action):

    def name(self) -> Text:
        return ACTION_SHOW_NEW_BOOKING_DETAILS

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

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
            dispatcher.utter_message(quickreplies=ResponseGenerator.quick_replies([QR_YES, QR_NO]))
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find the booking details.")

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
