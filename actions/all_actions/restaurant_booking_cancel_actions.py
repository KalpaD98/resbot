from actions.all_actions.common_imports_for_actions import *

ACTION_CANCEL_BOOKING = "action_cancel_booking"
ACTION_ASK_CANCEL_BOOKING_CONFIRMATION = "action_ask_cancel_booking_confirmation"


class ActionAskCancelBookingConfirmation(Action):
    def name(self) -> Text:
        return ACTION_ASK_CANCEL_BOOKING_CONFIRMATION

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Get the booking_id from the slot
            booking_id = tracker.get_slot(BOOKING_ID)
            # lang
            language = tracker.get_slot(LANGUAGE)

            if booking_id:
                # Fetch booking information from the database using booking_id
                booking = booking_repo.find_booking_by_id(booking_id)
                # Fetch restaurant data
                restaurant = restaurant_repo.find_restaurant_by_id(booking.restaurant_id)

                message = f"Are you sure you want to cancel the booking for {restaurant.name} on " \
                          f"{booking.date} for {booking.num_people} people? This action cannot be undone."

                if language == SIN:
                    message = f"ඔබට {restaurant.name}" \
                              f" හී {booking.date} දින සහභාගිවන්නන් {booking.num_people}" \
                              f" නියම වී ඇති booking එක අවලංගු කිරීමට අවශ්‍ය බව sure ද?" \
                              f" මෙම ක්‍රියාව අහෝසි කළ නොහැක."

                dispatcher.utter_message(text=message,
                                         quick_replies=ResponseGenerator.quick_reply_yes_no_with_payload())
            else:
                message = "Something went wrong. Please try again."
                if language == SIN:
                    message = "අසාර්ථකයි. නැවත උත්සාහ කරන්න."
                dispatcher.utter_message(text=message)

        except Exception as e:
            logger.error(f"An error occurred in ActionAskCancelBookingConfirmation: {e}")
            dispatcher.utter_message(text="An error occurred. Please try again later.")

        return []


class ActionCancelBooking(Action):
    def name(self) -> Text:
        return ACTION_CANCEL_BOOKING

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[EventType]:

        try:
            language = tracker.get_slot(LANGUAGE)
            booking_id = tracker.get_slot(BOOKING_ID)

            if booking_id is None:
                message = "No booking ID found. Please try again."
                if language == SIN:
                    message = "කිසිදු booking එකක් හමු නොවීය. නැවත උත්සාහ කරන්න."
                dispatcher.utter_message(text=message)
                return []

            # Fetch booking information from the database using booking_id (customize this part)
            booking = booking_repo.find_booking_by_id(booking_id)

            if booking is None:
                message = "No booking ID found. Please try again."
                if language == SIN:
                    message = "කිසිදු booking එකක් හමු නොවීය. නැවත උත්සාහ කරන්න."
                dispatcher.utter_message(text=message)
                return []

            restaurant = restaurant_repo.find_restaurant_by_id(booking.restaurant_id)

            if restaurant is None:
                message = "No restaurant found for the provided booking. Please try again."
                if language == SIN:
                    message = "ලබා දී ඇති booking සඳහා restaurant නැත. නැවත උත්සාහ කරන්න."
                dispatcher.utter_message(text=message)
                return []

            # Cancel the booking in the database using booking_id (customize this part)
            booking_repo.cancel_booking(booking_id)

            message = f"Your booking at {restaurant.name} on {booking.date} for {booking.num_people} " \
                      f"people has been successfully canceled."

            if language == SIN:
                message = f"ඔබගේ {restaurant.name} හි {booking.date} දින" \
                          f" පුද්ගලයින්ට {booking.num_people} සමඟ ඇති booking එක සාර්ථකව අවලංගු කරන ලදී."

            # Send the message to the user
            dispatcher.utter_message(text=message)

        except Exception as e:
            logger.error(f"An error occurred in ActionCancelBooking: {e}")
            dispatcher.utter_message(text="An error occurred. Please try again later.")

        # Clear the booking_id slot and return the event
        return [SlotSet("booking_id", None)]
