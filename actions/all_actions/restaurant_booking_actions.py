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

            # lang
            language = LanguageSelector.get_language(tracker)

            # send the message back to the user
            message = "You selected " + restaurant.name + '\n\n' + "Would you like to proceed with the booking?"

            if language == SIN:
                message = "ඔබ " + restaurant.name + '' + " හී table එකක් වෙන් කරවාගන්න කැමතිද?"

            dispatcher.utter_message(text=message,
                                     quick_replies=ResponseGenerator.
                                     quick_reply_yes_no_with_payload(language))
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

            # lang
            language = LanguageSelector.get_language(tracker)

            # send restaurant details to the user
            dispatcher.utter_message(image=restaurant.image_url)

            message = f"{restaurant.name} mainly serves {restaurant.cuisine} food and is located at " \
                      f"{restaurant.address}." \
                      f"\n\nTheir opening hours are:" \
                      f"\n\nMon - Fri: {restaurant.opening_hours[Restaurant.MON_TO_FRI]}" \
                      f"\n\nSat, Sun: {restaurant.opening_hours[Restaurant.SAT_SUN]}"

            if language == SIN:
                message = f"{restaurant.name} ප්රධාන වශයෙන් {restaurant.cuisine} ආහාර සදහා ප්‍රචලිත වේ." \
                          f"\n\n එය පිහිටා ඇත්තෙ " \
                          f"{restaurant.address} හීය" \
                          f"\n\nඔවුන්ගේ විවෘත වේලාවන් වන්නේ:" \
                          f"\n\nසඳු - සිකු: {restaurant.opening_hours[Restaurant.MON_TO_FRI]}" \
                          f"\n\nසෙනසුරාදා, ඉරිදා: {restaurant.opening_hours[Restaurant.SAT_SUN]}"

            dispatcher.utter_message(text=message)

            dispatcher.utter_message(text=ObjectUtils.get_random_sentence(
                restaurant.name,
                UTTER_SENTENCE_LIST_FOR_ASKING_TO_MAKE_RESERVATION if language == EN
                else UTTER_SENTENCE_LIST_FOR_ASKING_TO_MAKE_RESERVATION_SIN),

                quick_replies=ResponseGenerator.quick_reply_yes_no_with_payload(language))

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

            # get the date, time and num_people from the tracker
            date = tracker.get_slot("date")
            time = tracker.get_slot("time")
            num_people = tracker.get_slot("num_people")
            # since already selected restaurant is stored in the tracker, we can get it from there
            restaurant = tracker.get_slot(SELECTED_RESTAURANT)
            user = tracker.get_slot(LOGGED_USER)

            language = LanguageSelector.get_language(tracker)

            # for changing restaurant booking: do testing
            if restaurant is None:
                return [FollowupAction("action_validate_and_compare_booking_changes_ask_confirmation_to_change")]

            # send the message to the user

            details_message = f"{user[User.NAME]}, your booking summary for {restaurant[Restaurant.NAME]} " \
                              f"is as follows:" \
                              f"\n\nNumber of people: {num_people}" \
                              f"\n\nDate: {date}"
            details_message += f"\n\nTime: {time}" if time else ""

            message = "Would you like to confirm this booking?"

            if language == SIN:
                details_message = f"{user[User.NAME]}, {restaurant[Restaurant.NAME]} සඳහා ඔබේ booking සාරාංශය " \
                                  f" පහත පරිදි වේ:" \
                                  f"\n\nපුද්ගලයින් ගණන: {num_people}" \
                                  f"\n\nදිනය: {date}"
                details_message += f"\n\nවේලාව: {time}" if time else ""

                message = "ඔබට මෙම booking එක තහවුරු කිරීමට අවශ්‍යද?"

            dispatcher.utter_message(text=details_message)

            # ask to confirm the booking

            dispatcher.utter_message(text=message,
                                     quick_replies=ResponseGenerator.quick_reply_yes_no_with_payload(language))

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
            language = LanguageSelector.get_language(tracker)

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

            if language == SIN:
                booking_summary_message = "ඔබේ " + selected_restaurant[Restaurant.NAME] + " හි ඇති " \
                                          + selected_restaurant[Restaurant.ADDRESS] + \
                                          " booking එක" + date + " දිනයට තහවුරු කර ඇත"

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
