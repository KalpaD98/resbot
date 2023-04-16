from actions.all_actions.common_imports_for_actions import *

from actions.all_actions.helper_functions.restaurant_helper import get_restaurant
from submodules.database.models.restaurant import Restaurant

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
        print_all_slots(tracker)

        restaurant = get_restaurant(tracker, dispatcher)

        if restaurant is None:
            return []

        logging.info(restaurant)

        y_n_quick_replies_with_payload = []

        quick_reply_yes = {
            TITLE: QR_YES,
            PAYLOAD: "/affirm"}

        quick_reply_no = {
            TITLE: QR_NO,
            PAYLOAD: "/deny"}

        y_n_quick_replies_with_payload.append(quick_reply_yes)
        y_n_quick_replies_with_payload.append(quick_reply_no)
        # send the message back to the user
        dispatcher.utter_message(text="You selected " + restaurant.name)
        # add multiple messages for each below
        # dispatcher.utter_message(text="<small description>, <address>, <Opening hours [weekend,weekdays]>")
        dispatcher.utter_message(text="Would you like to proceed with the booking?",
                                 quick_replies=ResponseGenerator.quick_replies(y_n_quick_replies_with_payload, True))
        # if yes -> fill slot
        return [SlotSet(NUM_PEOPLE, None), SlotSet(DATE, None), SlotSet(TIME, None),
                SlotSet(SELECTED_RESTAURANT, restaurant.to_dict())]
        # if no
        # Clear the slots related to restaurant selection


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


# This function is used to generate a booking summary and send it to the user as a message.
class ActionShowBookingSummary(Action):

    # action name
    def name(self) -> Text:
        return ACTION_SHOW_BOOKING_SUMMARY

    # async run function to generate booking summary that include restaurant, restaurant address, date and time.

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print_all_slots(tracker)

        # get restaurant id from the tracker
        # restaurant_id = tracker.get_slot("restaurant_id")

        # get the date from the tracker
        date = tracker.get_slot("date")
        time = tracker.get_slot("time")
        num_people = tracker.get_slot("num_people")
        # since already selected restaurant is stored in the tracker, we can get it from there
        restaurant = tracker.get_slot(SELECTED_RESTAURANT)
        user = tracker.get_slot(LOGGED_USER)

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
                                 quick_replies=ResponseGenerator.quick_replies([QR_YES, QR_NO]))

        # TODO: if no -> ask if they would like to book a table of another restaurant or exit
        # TODO: if no -> ask if they would like to change booking details or exit
        # throw quick replies for above cases
        # change details -> clear slots and throw booking form again
        # exit -> clear slots and throw exit message, utter ask anything else QRs
        return []
        # if no clear restaurant  slots by far


# action_confirm_booking.
# This function is used to confirm the booking and send a message to the user based on their response.
# run this function after confirming the booking.
class ActionConfirmBooking(Action):
    def name(self) -> Text:
        return ACTION_CONFIRM_BOOKING

    # run method to confirm the booking, save on database and send a message to the user based on their response

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
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

        dispatcher.utter_message(text="Your booking id is: " + str(booking.id))

        # clear slots num_people, date, time, restaurant_id, selected_restaurant
        return [SlotSet(CUISINE, None), SlotSet(NUM_PEOPLE, None), SlotSet(DATE, None),
                SlotSet(TIME, None), SlotSet(RESTAURANT_ID, None), SlotSet(SELECTED_RESTAURANT, None)]
