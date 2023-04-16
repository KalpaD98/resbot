from actions.all_actions.common_imports_for_actions import *

ACTION_CHANGE_RESTAURANT_BOOKING_DETAILS = "action_change_restaurant_booking_details"
ACTION_SHOW_NEW_BOOKING_DETAILS = "action_show_new_booking_details"


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
                    text=f"Your booking with ID {booking_id} has been successfully {' and '.join(update_messages)}.")

                return [SlotSet("date", None), SlotSet("num_people", None)]
            else:
                dispatcher.utter_message(text="No changes were made to your booking.")

        except Exception as e:
            logger.error(f"An error occurred in ActionChangeBookingDetails: {e}")
            dispatcher.utter_message(text="An error occurred. Please try again later.")

        return []
