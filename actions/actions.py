# Actions.py This files contains custom actions which can be used to run custom Python code.
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import logging
from typing import Any, Dict, List, Text

from rasa.core.actions.forms import FormAction
from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase

from actions.submodules.constants import *
from actions.submodules.mock_data import *
from actions.submodules.object_utils import ObjectUtil
from actions.submodules.response_generator import ResponseGenerator
from actions.submodules.slot_validation import SlotValidator

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
    #     # load knowledge base with data from the given file
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
        if (cuisine == 'any') or cuisine is None:
            text_msg = f"I've found some great restaurants for you to try out!"
        else:
            text_msg = f"I've found some great {cuisine.lower()} restaurants for you to try out!"

        # get the restaurant list from recommendation engine

        dispatcher.utter_message(text=text_msg,
                                 attachment=ResponseGenerator.card_options_carousal(
                                     ObjectUtil.restaurant_list_to_carousal_object(rest_list)))

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
                                     ObjectUtil.restaurant_list_to_carousal_object(rest_list)))
        if rest_list is None:
            dispatcher.utter_message(text="Sorry, I did not find any more restaurants.")

        return []


# action_show_selected_restaurant_details.
# This function will fetch data of the selected restaurant and send it in the message.
# This will include a small description about the restaurant, its address and opening hours.
class ActionShowSelectedRestaurantDetails(Action):
    def name(self) -> Text:
        return ACTION_SHOW_SELECTED_RESTAURANT_DETAILS

    # async run function to fetch restaurant data from the knowledge base

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print_slots(tracker)

        # get the restaurant id from the tracker
        restaurant_id = tracker.get_slot("restaurant_id")

        if restaurant_id is None:
            dispatcher.utter_message(text="Cannot show restaurant details. Please select a restaurant first.")
            return []

        # restaurant = await self.knowledge_base.get_object("restaurant", restaurant_id)

        # Send the image to the user
        # dispatcher.utter_message(image=image_path)

        # get the restaurant details by passing the id
        restaurant = ObjectUtil.find_by_id(restaurant_id, rest_list)
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
            text=ObjectUtil.get_random_sentence(restaurant[NAME], UTTER_SENTENCE_LIST_FOR_ASKING_TO_MAKE_RESERVATION),
            quick_replies=ResponseGenerator.quick_replies([QR_YES, QR_NO]))

        return [SlotSet("selected_restaurant", restaurant), SlotSet("restaurant_id", restaurant_id)]


# action_select_restaurant_ask_booking_confirmation.
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
        restaurant = ObjectUtil.find_by_id(restaurant_id, rest_list)
        logging.info(restaurant)

        # send the message back to the user
        dispatcher.utter_message(text="You selected " + restaurant[NAME])
        # add multiple messages for each below
        # dispatcher.utter_message(text="<small description>, <address>, <Opening hours [weekend,weekdays]>")
        dispatcher.utter_message(text="Would you like to proceed with the booking?",
                                 quick_replies=ResponseGenerator.quick_replies([QR_YES, QR_NO]))
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

        # get the restaurant data from the knowledge base
        # restaurant = await self.knowledge_base.get_object("restaurant", restaurant_id)

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

        # get the restaurant data from the knowledge base
        # restaurant = self.knowledge_base.get_object("restaurant", restaurant_id)

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
        is_valid, message = SlotValidator.validate_restaurant_id(restaurant_id)

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
        is_valid, message = SlotValidator.validate_num_people(num_people)

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
        is_valid, date_value, message = SlotValidator.validate_date(date)

        if is_valid:
            return [SlotSet(date_slot, date_value)]
        else:
            dispatcher.utter_message(text=message)
            return [SlotSet(date_slot, None), FollowupAction("action_ask_date")]


class DateForm(FormAction):
    def name(self) -> Text:
        return "action_date_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["date"]

    def slot_mappings(self) -> Dict[Text, Any]:
        return {
            "date": self.from_entity(entity="date", intent="inform_date"),
        }

    async def validate_date(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        is_valid, date_value, message = SlotValidator.validate_date(value)
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
        is_valid, time_value, message = SlotValidator.validate_time(time)

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
        is_valid, message = SlotValidator.validate_user_id(user_id)

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
        is_valid, message = SlotValidator.validate_cuisine(cuisine)

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
        is_valid, message = SlotValidator.validate_booking_reference_id(booking_reference_id)

        if is_valid:
            return [SlotSet(BOOKING_REFERENCE_ID, booking_reference_id)]
        else:
            dispatcher.utter_message(text=message)
            return [SlotSet(BOOKING_REFERENCE_ID, None)]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# --------------------------------------------- Form Validation Actions --------------------------------------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


############# include below to run above action #############
#
# rules:
# - rule: Validate date
#   steps:
#   - intent: inform_date
#   - action: action_validate_date
#   - slot_was_set:
#     - date: null

# --------------------------------------------------------- #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# --------------------------------------------- Knowledge Base Actions ---------------------------------------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# action to show top restaurants based on user preferences and the given cuisine (or without specific cuisine).
class ActionQueryKnowledgeBase(Action):

    def __init__(self):
        # load knowledge base with data from the given file

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

######## Important Commented Code ########


# Vanilla JS UI

# this is for vanilla JS UI
# data = [{"title": cuisine, "payload": cuisine + "_payload"} for cuisine in cuisines]

# # This is working for normal UI
# message = {"payload": "quickReplies", "data": data}
#

#
# class ValidateRestaurantBookingForm(FormValidationAction):
#     def name(self) -> Text:
#         return VALIDATE_RESTAURANT_BOOKING_FORM
#
#     async def run(
#             self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> List[EventType]:
#         # Extract all slot values
#         slot_values = await self.extract_slots(dispatcher, tracker, domain)
#         validation_output = await self.validate(dispatcher, tracker, domain)
#
#         # Update the tracker with the extracted slots
#         for slot, value in slot_values.items():
#             if slot not in validation_output:
#                 validation_output[slot] = {"value": value}
#
#         # Get the list of required slots
#         required_slots = await self.required_slots(
#             self.slots_mapped_in_domain(domain), dispatcher, tracker, domain
#         )
#
#         # Check if any slot has an error
#         has_error = False
#         for slot, value in validation_output.items():
#             if value is None:
#                 has_error = True
#                 break
#
#         # If there is an error or not all required slots are filled and validated, return the validation output
#         if has_error or not all(tracker.get_slot(slot) for slot in required_slots):
#             return [SlotSet(slot, value) for slot, value in validation_output.items()]
#
#         # If all slots are filled and validated, deactivate the form and return the extracted slots
#         return await self.deactivate()
#
#     async def required_slots(
#             self,
#             slots_mapped_in_domain: List[Text],
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> List[Text]:
#         required_slots_list = [slot for slot in slots_mapped_in_domain if not tracker.get_slot(slot)]
#         print("Required slots: ", required_slots_list)
#         return required_slots_list
#
#     async def extract_slots(
#             self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:
#         slot_values = await super().extract_slots(dispatcher, tracker, domain)
#         print("Extracted slots: ", slot_values)
#         return slot_values
#
#     async def validate_date(
#             self,
#             slot_value: Any,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:
#         is_valid, date, message = SlotValidator.validate_date(slot_value)
#         if is_valid:
#             return {"date": date}
#         else:
#             dispatcher.utter_message(text=message)
#             return {"date": None}
#
#     async def validate_restaurant_id(
#             self,
#             slot_value: Any,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:
#         is_valid, message = SlotValidator.validate_restaurant_id(slot_value)
#         if is_valid:
#             return {"restaurant_id": slot_value}
#         else:
#             dispatcher.utter_message(text=message)
#             return {"restaurant_id": None}
#
#     async def validate_num_people(
#             self,
#             slot_value: Any,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:
#
#         is_valid, message = SlotValidator.validate_num_people(slot_value)
#
#         if is_valid:
#             return {"num_people": slot_value}
#         else:
#             dispatcher.utter_message(text=message)
#             return {"num_people": None}
#
#     async def deactivate(self) -> List[EventType]:
#         return [ActiveLoop(None), SlotSet("requested_slot", None)]


class ActionValidateDate(Action):
    def name(self) -> Text:
        return ACTION_VALIDATE_DATE

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[EventType]:
        date = tracker.get_slot(DATE)
        is_valid, date_value, message = SlotValidator.validate_date(date)

        if is_valid:
            return [SlotSet(DATE, date_value)]
        else:
            dispatcher.utter_message(text=message)
            return [SlotSet(DATE, None)]

# class ActionAskDate(Action):
#     def name(self) -> Text:
#         return "action_ask_date"
#
#     async def run(
#             self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> List[EventType]:
#         date_slot = "date"
#         date = tracker.get_slot(date_slot)
#         is_valid, date_value, message = SlotValidator.validate_date(date)
#
#         while not is_valid:
#             dispatcher.utter_message(text=message)
#             date = await self._ask_date(dispatcher)
#             is_valid, date_value, message = SlotValidator.validate_date(date)
#
#         return [SlotSet(date_slot, date_value)]
#
#     @staticmethod
#     async def _ask_date(dispatcher: CollectingDispatcher) -> str:
#         date_event = await dispatcher.event_input({"type": "slot", "name": "date"})
#         return date_event["value"]
