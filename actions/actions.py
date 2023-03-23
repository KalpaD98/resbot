# Actions.py This files contains custom actions which can be used to run custom Python code.
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import logging
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import (SlotSet)
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase

from actions.submodules.constants import *
from actions.submodules.mock_data import *
from actions.submodules.object_utils import ObjectUtil
from actions.submodules.response_generator import ResponseGenerator


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
        cuisines = ['any', 'italian', 'mexican', 'vietnamese', 'thai', 'japanese', 'korean']

        # generate synonyms for 'Any' cuisine
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

        print('\n--------------------------------------------------------Slots----------------------------------------')
        logging.info(tracker.slots)
        print('-----------------------------------------------------------------------------------------------------\n')

        # get cuisine from the tracker
        cuisine = tracker.get_slot("cuisine")

        # if cuisine is 'Any Cuisine' then don't filter by cuisine

        # if cuisine is null ask if user wants to filter by cuisine
        if cuisine is None:
            logging.info("Cuisine not set")
        else:
            logging.info("Cuisine: " + cuisine)

        # if yes then ask for cuisine (utter_ask_cuisine)

        # if no then send http request to recommendation engine to get top 10 restaurants for the user

        # send http request to recommendation engine to get top 10 restaurants for the user

        # every restaurant must have a 'name', 'image' (URL), id, ratings (1 - 5) and cuisine.

        # get restaurant data into an array

        # hard coded restaurant data
        text_msg = f"I've found some great {cuisine.lower()} restaurants for you to try out!"
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
        # print slots
        print('\n----------------------Slots-----------------------------------')
        logging.info(tracker.slots)
        print('--------------------------------------------------------------------\n')

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
        print('\n----------------------Slots-----------------------------------')
        logging.info(tracker.slots)
        print('--------------------------------------------------------------------\n')

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

        return [SlotSet("selected_restaurant", restaurant)]


# action_select_restaurant_ask_booking_confirmation.
class ActionBookSelectedRestaurant(Action):
    def name(self) -> Text:
        return ACTION_SHOW_SELECTED_RESTAURANT_ASK_BOOKING_CONFIRMATION

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # print slots
        print('\n----------------------Slots-----------------------------------')
        logging.info(tracker.slots)
        print('--------------------------------------------------------------------\n')

        # get the restaurant id from the tracker
        restaurant_id = tracker.get_slot("restaurant_id")

        if restaurant_id is None:
            logging.info("Restaurant ID not set")
            dispatcher.utter_message(text="Cannot show restaurant details. Please select a restaurant first.")
            return []

        # get the restaurant details by passing the id
        restaurant = ObjectUtil.find_by_id(rest_list, restaurant_id)
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
        print('\n----------------------Slots-----------------------------------')
        logging.info(tracker.slots)
        print('--------------------------------------------------------------------\n')

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
        print('\n----------------------Slots-----------------------------------')
        logging.info(tracker.slots)
        print('--------------------------------------------------------------------\n')

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
        message = "Your booking for" + selected_restaurant[NAME] + " located at " + selected_restaurant[ADDRESS] + \
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

        quick_replies_with_payload.append(quick_reply_show_more)
        quick_replies_with_payload.append(quick_reply_search_restaurant)

        dispatcher.utter_message(text="Is there anything else I can help you with?",
                                 quick_replies=ResponseGenerator.quick_replies(quick_replies_with_payload, True))
        return []


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
        # get details from tracker

        # tracker.get_slot("")
        # tracker.get_slot("cuisine")

        return []

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
