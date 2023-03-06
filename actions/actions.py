# Actions.py This files contains custom actions which can be used to run custom Python code.
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import json
from typing import Any, Text, Dict, List

from SPARQLWrapper import SPARQLWrapper, JSON
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase

from actions.submodules.mock_data import *


# action to show top cuisines based on user preferences
class ActionShowCuisines(Action):
    def name(self) -> Text:
        return "action_show_cuisines"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # get top 10 personalised cuisines for a particular user from the recommendation engine

        cuisines = ['Any Cuisine', 'Italian', 'Mexican', 'Vietnamese', 'Thai', 'Japanese', 'Korean']

        data = [{"title": cuisine, "payload": cuisine + "_payload"} for cuisine in cuisines]

        # This is working for normal UI
        message = {"payload": "quickReplies", "data": data}
        dispatcher.utter_message(text="Please choose a cuisine", json_message=message)

        # this is for bot front web-chat

        # dispatcher.utter_message(text="Do you want me to find a perfect hotel that can you can fit in for a Din ? ",
        #                          quick_replies=[{"title": "Italian"},
        #                                         {"title": "Chinese"}])

        return []


# action to show top restaurants based on user preferences and the given cuisine
class ActionShowRestaurantFilterByCuisine(Action):
    def __init__(self):
        # load knowledge base with data from the given file

        kb = InMemoryKnowledgeBase("knowledge_base_data.json")

        # overwrite the representation function of the restaurant object
        # by default the representation function is just the name of the object

        kb.set_representation_function_of_object(
            "restaurant", lambda obj: obj["name"] + "(" + obj["cuisine"] + ")"
        )

        super().__init__(kb)

    def name(self) -> Text:
        return "action_show_restaurants_filter_by_cuisine"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # get cuisine from the tracker
        cuisine = tracker.get_slot("cuisine")

        # if cuisine is 'Any Cuisine' then don't filter by cuisine

        # send http request with cuisine to recommendation engine to get top 10 restaurants for the user

        # get restaurant data into an array
        # every restaurant must have a 'name', 'image' (URL), id, ratings (1 - 5) and cuisine.

        # hard coded restaurant data

        rest_list = json.loads(restaurants)

        data_set = []

        for i in range(len(rest_list)):
            data_set.insert(i, rest_list[i])

        data = {
            "payload": 'cardsCarousel',
            "data": data_set
        }

        dispatcher.utter_message(json_message=data)

        return []


# action_show_selected_restaurant_details.
# This function will fetch data of the selected restaurant and send it in the message.
# This will include a small description about the restaurant, its address and opening hours.
class ActionShowSelectedRestaurantDetails(Action):
    def name(self) -> Text:
        return "action_show_selected_restaurant_details"

    # async run function to fetch restaurant data from the knowledge base

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # get the restaurant id from the tracker
        restaurant_id = tracker.get_slot("restaurant")

        # get the restaurant data from the knowledge base
        restaurant = await self.knowledge_base.get_object("restaurant", restaurant_id)

        # create a message to show the restaurant details
        message = "Here are some details about the restaurant: \n"
        message += "Name: " + restaurant["name"] + "\n"
        message += "Address: " + restaurant["address"] + "\n"
        message += "Open: " + restaurant["open"] + "\n"
        message += "Close: " + restaurant["close"] + "\n"
        message += "Description: " + restaurant["description"] + "\n"

        # send the message back to the user
        dispatcher.utter_message(text=message)
        return []


# action_show_booking_summary.
# This function is used to generate a booking summary and send it to the user as a message.
class ActionShowBookingSummary(Action):

    # action name
    def name(self) -> Text:
        return "action_show_booking_summary"

    # async run function to generate booking summary that include restaurant, restaurant address, date and time.

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # get restaurant id from the tracker
        restaurant_id = tracker.get_slot("restaurant_id")

        # get the restaurant data from the knowledge base
        restaurant = await self.knowledge_base.get_object("restaurant", restaurant_id)

        # get the date from the tracker
        date = tracker.get_slot("date")

        # get the time from the tracker
        time = tracker.get_slot("time")

        # generate the booking summary
        message = "Shall I confirm your booking for " + restaurant["name"] + " located at " + restaurant["address"] + \
                  "on " + date + " at " + time + "."

        # add a response after this asking if the user would like to confirm the booking
        # send the message to the user
        dispatcher.utter_message(text=message)
        return []


# action_confirm_booking.
# This function is used to confirm the booking and send a message to the user based on their response.
# run this function after confirming the booking.
class ActionConfirmBooking(Action):
    def name(self) -> Text:
        return "action_confirm_booking"

    # run method to confirm the booking, save on database and send a message to the user based on their response

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # get the restaurant id from the tracker
        restaurant_id = tracker.get_slot("restaurant_id")

        # get the restaurant data from the knowledge base
        restaurant = self.knowledge_base.get_object("restaurant", restaurant_id)

        # get the date from the tracker
        date_time = tracker.get_slot("date_time")

        # extract the date from the date_time slot
        date = date_time.split("T")[0]

        # extract the time from the date_time slot
        time = date_time.split("T")[1]

        # generate the booking summary
        message = "Your booking for " + restaurant["name"] + " located at " + restaurant["address"] + \
                  "on " + date + " at " + time + " has been confirmed. Thank you for using our service."

        # send the message to the user
        dispatcher.utter_message(text=message)
        return []


# action_request_more_restaurant_options.
# This function is used to pull more restaurant options for the user if they request for more.
class ActionRequestMoreRestaurantOptions(Action):

    def name(self) -> Text:
        return "action_request_more_restaurant_options"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # get more restaurants from the knowledge base that are not in the list of restaurants already shown to the user

        # if there are more restaurants, send them to the user

        # else send a message to the user saying that there are no more restaurants
        dispatcher.utter_message(text="Sorry, I did not find any more restaurants. "
                                      "Please try again with a different "
                                      "cuisine.")

        return []
