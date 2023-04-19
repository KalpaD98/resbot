from actions.all_actions.common_imports_for_actions import *

from actions.all_actions.helper_functions.restaurant_helper import get_restaurant
from submodules.database.data_models.restaurant import Restaurant

# constants
ACTION_SHOW_SELECTED_RESTAURANT_DETAILS = "action_show_selected_restaurant_details"
ACTION_SHOW_SELECTED_RESTAURANT_ASK_BOOKING_CONFIRMATION = "action_show_selected_restaurant_ask_booking_confirmation"
ACTION_SHOW_BOOKING_SUMMARY = "action_show_booking_summary"
ACTION_CONFIRM_BOOKING = "action_confirm_booking"


# action_show_selected_restaurant_ask_booking_confirmation.
class ActionShowSelectedRestaurantAskBookingConfirmation(Action):
    def name(self) -> Text:
        return ACTION_SHOW_SELECTED_RESTAURANT_ASK_BOOKING_CONFIRMATION

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            print_all_slots(tracker)

            restaurant = get_restaurant(tracker, dispatcher)

            if restaurant is None:
                return []

            logging.info(restaurant)

            # send the message back to the user
            dispatcher.utter_message(text="You selected " + restaurant.name)
            # add multiple messages for each below
            # dispatcher.utter_message(text="<small description>, <address>, <Opening hours [weekend,weekdays]>")
            dispatcher.utter_message(text="Would you like to proceed with the booking?",
                                     quick_replies=ResponseGenerator.quick_reply_yes_no_with_payload())
            # if yes -> fill slot else remove prev slots
            return [SlotSet(NUM_PEOPLE, None), SlotSet(DATE, None), SlotSet(TIME, None),
                    SlotSet(SELECTED_RESTAURANT, restaurant.to_dict())]

        except Exception as e:
            logging.error(f"Error in ActionShowSelectedRestaurantAskBookingConfirmation: {e}")
            dispatcher.utter_message(text="Something went wrong. Please try again later.")

        return [SlotSet(NUM_PEOPLE, None), SlotSet(DATE, None), SlotSet(TIME, None), SlotSet(SELECTED_RESTAURANT, None)]


# action_show_selected_restaurant_details.
# This function will fetch data of the selected restaurant and send it in the message.
# This will include a small description about the restaurant, its address and opening hours.
class ActionShowSelectedRestaurantDetails(Action):
    def name(self) -> Text:
        return ACTION_SHOW_SELECTED_RESTAURANT_DETAILS

    # async run function to fetch restaurant data from the db_knowledge base
    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            print_all_slots(tracker)

            restaurant = get_restaurant(tracker, dispatcher)

            if restaurant is None:
                return []

            # send restaurant details to the user
            dispatcher.utter_message(image=restaurant.image_url)
            dispatcher.utter_message(
                text=restaurant.name + " mainly serves " + restaurant.cuisine
                     + " food and its located at " + restaurant.address)
            dispatcher.utter_message(text="Their opening hours are, ")
            dispatcher.utter_message(text="Mon - Fri: " + restaurant.opening_hours[Restaurant.MON_TO_FRI])
            dispatcher.utter_message(text="Sat - Sun: " + restaurant.opening_hours[Restaurant.SAT_SUN])

            dispatcher.utter_message(text=ObjectUtils.get_random_sentence(restaurant.name,
                                                                          UTTER_SENTENCE_LIST_FOR_ASKING_TO_MAKE_RESERVATION),
                                     quick_replies=ResponseGenerator.quick_reply_yes_no_with_payload())

            return [SlotSet(NUM_PEOPLE, None), SlotSet(DATE, None), SlotSet(TIME, None),
                    SlotSet(SELECTED_RESTAURANT, restaurant.to_dict())]
        except Exception as e:
            # Log the error and inform the user
            logger.error(f"Error in ActionShowSelectedRestaurantDetails: {e}")
            dispatcher.utter_message(
                text="Sorry, I encountered an error while showing the restaurant details. Please try again.")
            return []


# This function is used to generate a booking summary and send it to the user as a message.
# if no -> ask if they would like to book a table of another restaurant or exit
# if no -> ask if they would like to change booking details or exit
# throw quick replies for above cases
# change details -> clear slots and throw booking form again
# exit -> clear slots and throw exit message, utter ask anything else QRs
# if no clear restaurant slots by far
class ActionShowBookingSummary(Action):

    def name(self) -> Text:
        return ACTION_SHOW_BOOKING_SUMMARY

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            print_all_slots(tracker)

            # get the date from the tracker
            date = tracker.get_slot("date")
            time = tracker.get_slot("time")
            num_people = tracker.get_slot("num_people")
            # since already selected restaurant is stored in the tracker, we can get it from there
            restaurant = tracker.get_slot(SELECTED_RESTAURANT)
            user = tracker.get_slot(LOGGED_USER)

            # for changing restaurant booking: do testing
            if restaurant is None:
                return [FollowupAction("action_validate_and_compare_booking_changes_ask_confirmation_to_change")]

            # send the message to the user
            dispatcher.utter_message(
                text=user[User.NAME] + ", your booking summary for " + restaurant[Restaurant.NAME] + " is as follows:")
            # generate the booking summary
            dispatcher.utter_message(text="Number of people: " + num_people)
            dispatcher.utter_message(text="Date: " + date)
            if time is not None:
                dispatcher.utter_message(text="Time: " + time)

            # ask to confirm the booking
            dispatcher.utter_message(text="Would you like to confirm this booking?",
                                     quick_replies=ResponseGenerator.quick_reply_yes_no_with_payload())


        except Exception as e:
            # Log the error and inform the user
            logger.error(f"Error in ActionShowBookingSummary: {e}")
            dispatcher.utter_message(
                text="Sorry, I encountered an error while showing the booking summary. Please try again.")

        return []


# This function is used to confirm the booking and send a message to the user based on their response.
# run this function after confirming the booking.
class ActionConfirmBooking(Action):
    def name(self) -> Text:
        return ACTION_CONFIRM_BOOKING

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            print_all_slots(tracker)

            # get the date from the tracker
            num_people = tracker.get_slot(NUM_PEOPLE)
            date = tracker.get_slot(DATE)
            time = tracker.get_slot(TIME)
            user_id = tracker.get_slot(USER_ID)

            if date is None or num_people is None:
                logging.error("Some values are missing in the booking confirmation")
                return []

            if user_id is None:
                logging.error("User id is missing in the booking confirmation")
                return []

            selected_restaurant = tracker.get_slot(SELECTED_RESTAURANT)

            restaurant_id = selected_restaurant[Restaurant.ID]

            booking = Booking(user_id, restaurant_id, num_people, date, time)
            booking_repo.insert_booking(booking)

            # send a booking_summary_message to the user
            booking_summary_message = "Your booking for " + selected_restaurant[Restaurant.NAME] + " located at " \
                                      + selected_restaurant[Restaurant.ADDRESS] + \
                                      " on " + date + " has been confirmed"

            dispatcher.utter_message(text=booking_summary_message)

            # dispatcher.utter_message(text="Your booking id is: " + str(booking.id))

            # clear slots num_people, date, time, restaurant_id, selected_restaurant
            return [SlotSet(CUISINE, None), SlotSet(NUM_PEOPLE, None), SlotSet(DATE, None),
                    SlotSet(TIME, None), SlotSet(RESTAURANT_ID, None), SlotSet(SELECTED_RESTAURANT, None)]
        except Exception as e:
            # Log the error and inform the user
            logger.error(f"Error in ActionConfirmBooking: {e}")
            dispatcher.utter_message(
                text="Sorry, I encountered an error while confirming the booking. Please try again.")
            return []
