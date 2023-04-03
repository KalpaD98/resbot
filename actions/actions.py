# Actions.py This files contains custom actions which can be used to run custom Python code.
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import logging
from typing import Any, Dict, List, Text, Optional

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import FollowupAction, SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase

from actions.submodules.constants.constants import *
from actions.submodules.entities.user import User
from actions.submodules.persistance.bookings import get_user_bookings
from actions.submodules.utils.mock_data_utils import *
from actions.submodules.utils.object_utils import ObjectUtils
from actions.submodules.utils.response_generation_utils import ResponseGenerator
from actions.submodules.utils.restaurant_response_generation_utils import RestaurantResponseGenerationUtils
from actions.submodules.utils.slot_validation_utils import SlotValidators

logger = logging.getLogger(__name__)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ----------------------------------------------- Restaurant Actions ------------------------------------------------ #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# action to show top cuisines based on user preferences.
# This will be shown as a quick reply.
class ActionShowCuisines(Action):
    def name(self) -> Text:
        return ACTION_SHOW_CUISINES

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # get top 10 personalised cuisines for a particular user from the recommendation engine or most popular
        # (frequent)
        cuisines = ['italian', 'mexican', 'vietnamese', 'thai', 'japanese', 'korean']

        cuisines.append('any cuisine')  # generate synonyms for 'Any' cuisine

        # Add payload to quick replies
        cuisines_with_entity_payload = []
        for cuisine in cuisines:
            # cuisines_with_entity_payload.append({TITLE: cuisine, PAYLOAD: cuisine})
            cuisines_with_entity_payload.append({
                TITLE: cuisine.capitalize(),
                PAYLOAD: "/inform_cuisine{\"cuisine\":\"" + cuisine.lower() + "\"}"})

        # Generate quick replies with Response Generator
        quick_replies_cuisines = ResponseGenerator.quick_replies(cuisines_with_entity_payload, with_payload=True)

        dispatcher.utter_message(text="Please choose a cuisine", quick_replies=quick_replies_cuisines)

        return []


# action to show top restaurants based on user preferences and the given cuisine (or without specific cuisine).
class ActionShowRestaurants(Action):

    # constructor
    # def __init__(self):
    #     # load db_knowledge base with data from the given file
    #     kb = InMemoryKnowledgeBase("knowledge_base_data.json")

    def name(self) -> Text:
        return ACTION_SHOW_RESTAURANTS

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get cuisine from the tracker
        cuisine = tracker.get_slot("cuisine")

        # if cuisine is 'Any Cuisine' then don't filter by cuisine

        # if cuisine is null ask if user wants to filter by cuisine
        if cuisine is None:
            return [FollowupAction(ACTION_SHOW_CUISINES)]
        else:
            logging.info("Cuisine: " + cuisine)

        # if yes then ask for cuisine (utter_ask_cuisine)

        # if no then send http request to recommendation engine to get top 10 restaurants for the user

        # send http request to recommendation engine to get top 10 restaurants for the user

        # every restaurant must have a 'name', 'image' (URL), id, ratings (1 - 5) and cuisine.

        # get restaurant data into an array

        # hard coded restaurant data
        if (cuisine == 'any cuisine') or cuisine is None:
            text_msg = f"I've found some great restaurants for you to try out!"
        else:
            text_msg = f"I've found some great {cuisine.lower()} restaurants for you to try out!"

        # get the restaurant list from recommendation engine

        dispatcher.utter_message(text=text_msg,
                                 attachment=ResponseGenerator.card_options_carousal(
                                     RestaurantResponseGenerationUtils.restaurant_list_to_carousal_object(rest_list)))

        return []


# TODO: action_request_more_restaurant_options.
# This function is used to pull more restaurant options for the user if they request for more.
class ActionRequestMoreRestaurantOptions(Action):

    def name(self) -> Text:
        return ACTION_SHOW_MORE_RESTAURANT_OPTIONS

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print_slots(tracker)

        dispatcher.utter_message(text="Here are some more restaurants I found",
                                 attachment=ResponseGenerator.card_options_carousal(
                                     RestaurantResponseGenerationUtils.restaurant_list_to_carousal_object(rest_list)))
        if rest_list is None:
            dispatcher.utter_message(text="Sorry, I did not find any more restaurants.")

        return []


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
        print_slots(tracker)

        # get the restaurant id from the tracker
        restaurant_id = tracker.get_slot("restaurant_id")

        if restaurant_id is None:
            dispatcher.utter_message(text="Cannot show restaurant details. Please select a restaurant first.")
            return []

        # restaurant = await self.db_knowledge.get_object("restaurant", restaurant_id)

        # Send the image to the user
        # dispatcher.utter_message(image=image_path)

        # get the restaurant details by passing the id
        restaurant = ObjectUtils.find_by_id(restaurant_id, rest_list)
        logging.info(restaurant)

        # send the message back to the user

        dispatcher.utter_message(image=restaurant[IMAGE_URL])
        dispatcher.utter_message(
            text=restaurant[NAME] + " mainly serves " + restaurant[CUISINE] + " food and its located at "
                                                                              "" + restaurant[ADDRESS])
        dispatcher.utter_message(text="Their opening hours are, ")
        dispatcher.utter_message(text="Mon - Fri: " + restaurant[OPENING_HOURS][MON_TO_FRI])
        dispatcher.utter_message(text="Sat - Sun: " + restaurant[OPENING_HOURS][SAT_SUN])

        dispatcher.utter_message(
            text=ObjectUtils.get_random_sentence(restaurant[NAME], UTTER_SENTENCE_LIST_FOR_ASKING_TO_MAKE_RESERVATION),
            quick_replies=ResponseGenerator.quick_replies([QR_YES, QR_NO]))

        return [SlotSet("selected_restaurant", restaurant), SlotSet("restaurant_id", restaurant_id)]


# action_show_selected_restaurant_ask_booking_confirmation.
class ActionBookSelectedRestaurant(Action):
    def name(self) -> Text:
        return ACTION_SHOW_SELECTED_RESTAURANT_ASK_BOOKING_CONFIRMATION

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print_slots(tracker)

        # get the restaurant id from the tracker
        restaurant_id = tracker.get_slot("restaurant_id")

        if restaurant_id is None:
            logging.info("Restaurant ID not set")
            dispatcher.utter_message(text="Cannot show restaurant details. Please select a restaurant first.")
            return []

        # get the restaurant details by passing the id
        restaurant = ObjectUtils.find_by_id(restaurant_id, rest_list)
        # logging.info(restaurant)

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
        dispatcher.utter_message(text="You selected " + restaurant[NAME])
        # add multiple messages for each below
        # dispatcher.utter_message(text="<small description>, <address>, <Opening hours [weekend,weekdays]>")
        dispatcher.utter_message(text="Would you like to proceed with the booking?",
                                 quick_replies=ResponseGenerator.quick_replies(y_n_quick_replies_with_payload, True))
        # if yes -> fill slot
        return [SlotSet(SELECTED_RESTAURANT, restaurant)]
        # if no
        # Clear the slots related to restaurant selection


# action_show_booking_summary.
# This function is used to generate a booking summary and send it to the user as a message.
class ActionShowBookingSummary(Action):

    # action name
    def name(self) -> Text:
        return ACTION_SHOW_BOOKING_SUMMARY

    # async run function to generate booking summary that include restaurant, restaurant address, date and time.

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print_slots(tracker)

        # get restaurant id from the tracker
        # restaurant_id = tracker.get_slot("restaurant_id")

        # get the restaurant data from the db_knowledge base
        # restaurant = await self.db_knowledge.get_object("restaurant", restaurant_id)

        # get the date from the tracker
        date = tracker.get_slot("date")
        time = tracker.get_slot("time")
        restaurant = tracker.get_slot(SELECTED_RESTAURANT)
        # send the message to the user
        dispatcher.utter_message(
            text="Your booking summary for " + restaurant[NAME] + " is as follows:")
        # generate the booking summary
        dispatcher.utter_message(text="Number of people: " + tracker.get_slot(NUM_PEOPLE))
        dispatcher.utter_message(text="Date: " + date)
        if time is not None:
            dispatcher.utter_message(text="Time: " + time)

        # ask to confirm the booking

        # TODO: if no -> ask if they would like to book a table of another restaurant or exit

        dispatcher.utter_message(text="Would you like to confirm this booking?",
                                 quick_replies=ResponseGenerator.quick_replies([QR_YES, QR_NO]))
        # "Please choose a cuisine",
        # if yes
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
        print_slots(tracker)

        # get the restaurant id from the tracker
        restaurant_id = tracker.get_slot("restaurant_id")
        user_id = tracker.get_slot("user_id")

        # get the restaurant data from the db_knowledge base
        # restaurant = self.db_knowledge.get_object("restaurant", restaurant_id)

        # get the date from the tracker
        date = tracker.get_slot("date")
        if date is None:
            logging.info("Date not set")

        selected_restaurant = tracker.get_slot(SELECTED_RESTAURANT)

        # generate the booking summary
        message = "Your booking for " + selected_restaurant[NAME] + " located at " + selected_restaurant[ADDRESS] + \
                  " on " + date + " has been confirmed"

        # send the message to the user
        dispatcher.utter_message(text=message)
        dispatcher.utter_message(text="Your booking reference id is: brid_1FK2H1G3")

        return []


# anything else with quick replies
class ActionAnythingElse(Action):
    def name(self) -> Text:
        return ACTION_ASK_ANYTHING_ELSE

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # quick replies for show more and search with payload
        quick_replies_with_payload = []

        quick_reply_show_more = {
            TITLE: QR_SHOW_MORE_RESTAURANTS,
            PAYLOAD: "/request_more_restaurant_options"}

        quick_reply_search_restaurant = {
            TITLE: QR_SEARCH_RESTAURANTS,
            PAYLOAD: "/want_to_search_restaurants"}

        quick_reply_no = {
            TITLE: "No thanks",
            PAYLOAD: "/stop"}

        quick_replies_with_payload.append(quick_reply_show_more)
        quick_replies_with_payload.append(quick_reply_search_restaurant)
        quick_replies_with_payload.append(quick_reply_no)

        dispatcher.utter_message(text="Is there anything else I can help you with?",
                                 quick_replies=ResponseGenerator.quick_replies(quick_replies_with_payload, True))
        return []


# user related actions
class ActionCompleteRegistration(Action):

    def name(self) -> Text:
        return "action_save_user_and_complete_registration"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot("user_name")
        user_email = tracker.get_slot("user_email")
        password = tracker.get_slot("password")

        # Create a UserDetails object and add it to the users list
        user = User(user_name, user_email, password)
        users.append(user)

        # Optionally, send a confirmation message to the user
        dispatcher.utter_message(text="Congratulations on completing your registration!")

        # utter the details of the user
        dispatcher.utter_message(text="Your details are as follows:")
        dispatcher.utter_message(text="Name: " + user_name)
        dispatcher.utter_message(text="Email: " + user_email)
        dispatcher.utter_message(text="Password: " + ObjectUtils.star_print(len(password)))

        return []


class ActionLoginUser(Action):
    def name(self) -> Text:
        return "action_login_user"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        login_email = tracker.get_slot("login_email")
        login_password = tracker.get_slot("login_password")

        user = None
        # user = user = find_user_by_email(login_email)
        for u in users:
            if u["email"] == login_email and u["password"] == login_password:
                user = u
                break

        if user:
            return [
                SlotSet("user_name", user["name"]),
                SlotSet("user_id", user["id"]),
                SlotSet("user_email", user["email"])
            ]
        else:
            dispatcher.utter_message(text="Email or password is incorrect.")
            return [
                SlotSet("user_name", None),
                SlotSet("user_id", None),
                SlotSet("user_email", None),
                FollowupAction(ACTION_RETRY_LOGIN_OR_STOP)
            ]


class ActionRetryLoginOrStop(Action):
    def name(self) -> Text:
        return ACTION_RETRY_LOGIN_OR_STOP

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        quick_replies_with_payload = []

        quick_reply_retry = {
            TITLE: "Retry",
            PAYLOAD: "/request_login_form"}

        quick_reply_stop = {
            TITLE: "Stop",
            PAYLOAD: "/stop"}

        quick_replies_with_payload.append(quick_reply_retry)
        quick_replies_with_payload.append(quick_reply_stop)

        dispatcher.utter_message(text="Would you like to retry logging in or stop?",
                                 quick_replies=ResponseGenerator.quick_replies(quick_replies_with_payload, True))

        return []


# booking related
class ActionShowUserBookings(Action):
    def name(self) -> Text:
        return "action_show_user_bookings"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any],
                  booking_type: str) -> List[Dict[Text, Any]]:
        user_id = tracker.get_slot("user_id")
        user_bookings = get_user_bookings(user_id, booking_type)

        # Prepare carousel items
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
        return "action_show_past_bookings"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return await super().run(dispatcher, tracker, domain, booking_type="past")


class ActionShowUpcomingBookings(ActionShowUserBookings):
    def name(self) -> Text:
        return "action_show_upcoming_bookings"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return await super().run(dispatcher, tracker, domain, booking_type="upcoming")


class ActionShowNewBookingDetails(Action):

    def name(self) -> Text:
        return "action_show_new_booking_details"

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


class ActionChangeBookingDate(Action):
    def name(self) -> Text:
        return "action_change_booking_date"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        booking_id = tracker.get_slot("booking_id")
        new_date = tracker.get_slot("date")

        # Update the booking date in system here.
        # call  API to update database.

        # Send a confirmation message to the user
        dispatcher.utter_message(text=f"Your booking with ID {booking_id} has been successfully updated to {new_date}.")
        return [SlotSet("date", None)]


class ActionAskCancelBookingConfirmation(Action):
    def name(self) -> Text:
        return "action_ask_cancel_booking_confirmation"

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

        message = f"Are you sure you want to cancel the booking for {booking['restaurant_name']} on {booking['booking_date']} for {booking['num_people']} people? This action cannot be undone."

        dispatcher.utter_message(text=message)

        return []


class ActionCancelBooking(Action):
    def name(self) -> Text:
        return "action_cancel_booking"

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


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# --------------------------------------------- Form Validation Actions --------------------------------------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class ValidateRegistrationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_registration_form"

    async def validate_name(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, name_value, message = SlotValidators.validate_user_name(value)
        if is_valid:
            return {"name": name_value}
        else:
            dispatcher.utter_message(text=message)
            return {"name": None}

    async def validate_email(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, email_value, message = SlotValidators.validate_email(value)
        if is_valid:
            return {"email": email_value}
        else:
            dispatcher.utter_message(text=message)
            return {"email": None}

    async def validate_password(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, password_value, message = SlotValidators.validate_password(value)
        if is_valid:
            return {"password": password_value}
        else:
            dispatcher.utter_message(text=message)
            return {"password": None}


class ValidateLoginForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_login_form"

    async def validate_login_email(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, email, error_message = SlotValidators.validate_email(slot_value)
        if is_valid:
            return {"login_email": email}
        else:
            dispatcher.utter_message(text=error_message)
            return {"login_email": None}

    async def validate_login_password(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, password, error_message = SlotValidators.validate_password(slot_value)
        if is_valid:
            return {"login_password": password}
        else:
            dispatcher.utter_message(text=error_message)
            return {"login_password": None}


class BookingForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_booking_form"

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Text]:
        return ["num_people", "date"]

    async def validate_num_people(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, message = SlotValidators.validate_num_people(value)
        if is_valid:
            return {"num_people": value}
        else:
            dispatcher.utter_message(text=message)
            return {"num_people": None}

    async def validate_date(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, date_value, message = SlotValidators.validate_date(value)
        if is_valid:
            return {"date": date_value}
        else:
            dispatcher.utter_message(text=message)
            return {"date": None}


class ChangeBookingDateForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_change_booking_date_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["date"]

    def validate_date(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            Dict[Text, Any]:
        is_valid, new_date, error_message = SlotValidators.validate_date(value)
        if not is_valid:
            dispatcher.utter_message(text=error_message)
            return {"date": None}
        else:
            return {"date": new_date}


# Add a function to find a user by email
def find_user_by_email(email: str) -> Optional[User]:
    # Implement the logic to find a user by email
    # You can use your MongoDB database to search for the user
    pass


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# --------------------------------------------- Knowledge Base Actions ---------------------------------------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# action to show top restaurants based on user preferences and the given cuisine (or without specific cuisine).
class ActionQueryKnowledgeBase(Action):

    def __init__(self):
        # load db_knowledge base with data from the given file

        kb = InMemoryKnowledgeBase("knowledge_base_data.json")

        # # overwrite the representation function of the restaurant object
        # # by default the representation function is just the name of the object
        #
        # kb.set_representation_function_of_object(
        #     "restaurant", lambda obj: obj["name"] + "(" + obj["cuisine"] + ")"
        # )
        #
        # super().__init__(kb)

    def name(self) -> Text:
        return ACTION_QUERY_KNOWLEDGE_BASE

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return []


# print all slot values from Tracker
def print_slots(tracker: Tracker):  # -> List[Dict[Text, Any]]:
    print()
    print("Slots with values:")
    empty_slots = []

    for slot in tracker.slots:
        value = tracker.get_slot(slot)
        if value is not None:
            print(slot, ":", value)
        else:
            empty_slots.append(slot)

    print("\nEmpty slots: ", ", ".join(empty_slots))
    print()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# --------------------------------------------- Slot Validation Actions --------------------------------------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class ActionValidateRestaurantId(Action):
    def name(self) -> Text:
        return ACTION_VALIDATE_RESTAURANT_ID

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[EventType]:
        restaurant_id = tracker.get_slot(RESTAURANT_ID)
        is_valid, message = SlotValidators.validate_restaurant_id(restaurant_id)

        if is_valid:
            return [SlotSet(RESTAURANT_ID, restaurant_id)]
        else:
            dispatcher.utter_message(text=message)
            return [SlotSet(RESTAURANT_ID, None)]


class ActionValidateNumPeople(Action):
    def name(self) -> Text:
        return ACTION_VALIDATE_NUM_PEOPLE

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[EventType]:
        num_people = tracker.get_slot(NUM_PEOPLE)
        is_valid, message = SlotValidators.validate_num_people(num_people)

        if is_valid:
            return [SlotSet(NUM_PEOPLE, num_people)]
        else:
            dispatcher.utter_message(text=message)
            return [SlotSet(NUM_PEOPLE, None)]


class ActionAskDate(Action):
    def name(self) -> Text:
        return "action_ask_date"

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[EventType]:
        dispatcher.utter_message(text="Can you please provide the date again")
        dispatcher.utter_message(text="you can enter the date in a format like dd/mm/yyyy or similar")
        return []


class ActionValidateDate(Action):
    def name(self) -> Text:
        return "action_validate_date"

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[EventType]:
        date_slot = "date"
        date = tracker.get_slot(date_slot)
        is_valid, date_value, message = SlotValidators.validate_date(date)

        if is_valid:
            return [SlotSet(date_slot, date_value)]
        else:
            dispatcher.utter_message(text=message)
            return [SlotSet(date_slot, None), FollowupAction("action_ask_date")]


class DateForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_date_form"

    async def validate_date(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, date_value, message = SlotValidators.validate_date(value)
        if is_valid:
            return {"date": date_value}
        else:
            dispatcher.utter_message(text=message)
            return {"date": None}


class ActionValidateTime(Action):
    def name(self) -> Text:
        return ACTION_VALIDATE_TIME

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[EventType]:
        time = tracker.get_slot(TIME)
        is_valid, time_value, message = SlotValidators.validate_time(time)

        if is_valid:
            return [SlotSet(TIME, time_value)]
        else:
            dispatcher.utter_message(text=message)
            return [SlotSet(TIME, None)]


class ActionValidateUserId(Action):
    def name(self) -> Text:
        return ACTION_VALIDATE_USER_ID

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[EventType]:
        user_id = tracker.get_slot(USER_ID)
        is_valid, message = SlotValidators.validate_user_id(user_id)

        if is_valid:
            return [SlotSet(USER_ID, user_id)]
        else:
            dispatcher.utter_message(text=message)
            return [SlotSet(USER_ID, None)]


class ActionValidateCuisine(Action):
    def name(self) -> Text:
        return ACTION_VALIDATE_CUISINE

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[EventType]:
        cuisine = tracker.get_slot(CUISINE)
        is_valid, message = SlotValidators.validate_cuisine(cuisine)

        if is_valid:
            return [SlotSet(CUISINE, cuisine)]
        else:
            dispatcher.utter_message(text=message)
            return [SlotSet(CUISINE, None)]


class ActionValidateBookingReferenceId(Action):
    def name(self) -> Text:
        return "action_validate_booking_reference_id"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        booking_reference_id = tracker.get_slot(BOOKING_REFERENCE_ID)
        is_valid, message = SlotValidators.validate_booking_reference_id(booking_reference_id)

        if is_valid:
            return [SlotSet(BOOKING_REFERENCE_ID, booking_reference_id)]
        else:
            dispatcher.utter_message(text=message)
            return [SlotSet(BOOKING_REFERENCE_ID, None)]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ------------------------------------------------- Commented Code -------------------------------------------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Executes the fallback action and goes back to the previous state of the dialogue
# class ActionDefaultFallback(Action):
#     def name(self) -> Text:
#         return ACTION_DEFAULT_FALLBACK_NAME
#
#     async def run(
#             self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(template="my_custom_fallback_template")
#
#         # Revert user message which led to fallback.
#         return [UserUtteranceReverted()]
