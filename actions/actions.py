# This files contains custom actions which can be used to run custom Python code.

# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase


# action to show top cuisines based on user preferences

class ActionShowCuisines(Action):
    def name(self) -> Text:
        return "action_show_cuisines"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # get top personalised for a particular user 5 or 10 cuisines
        # and display them after preferences are calculated

        cuisines = ['italian', 'Mexican', 'Vietnamese', 'Thai', 'Japanese', 'Korean']

        data = [{"title": cuisine, "payload": cuisine + "_payload"} for cuisine in cuisines]

        # THIS is working for normal UI
        message = {"payload": "quickReplies", "data": data}
        dispatcher.utter_message(text="Please choose a cuisine", json_message=message)

        # this is for botfront web-chat

        # dispatcher.utter_message(text="Do you want me to find a perfect hotel that can you can fit in for a dine ? ",
        #                          quick_replies=[{"title": "Italian"},
        #                                         {"title": "Chinese"}])

        return []


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

        # hard coded rest data
        restaurants = """
        [ {
              "title":"Taco Bell",
              "image":"https://b.zmtcdn.com/data/pictures/1/18602861/bd2825ec26c21ebdc945edb7df3b0d99.jpg",
              "id":"itmx_taco_bell",
              "ratings":"4.5",
              "cuisine": "Mexican"
           },
           {
              "title":"Danke",
              "image":"https://lh3.googleusercontent.com/p/AF1QipOs5oyEh2eqR1wHmLuL7WPvdkiqPjyJJdHEeCyI=w600-h0",
              "id":"itmx_danke",
              "ratings":"5.0",
              "cuisine": "Italian"
           },
           {
              "id":2,
              "title":"I due forni",
              "image":"https://b.zmtcdn.com/data/pictures/4/18357374/661d0edd484343c669da600a272e2256.jpg",
              "id":"itmx_i_due_forni",
              "ratings":"4",
              "cuisine": "Italian"
           },
           {
              "title":"Lụa Restaurant",
              "image":"https://www.collinsdictionary.com/images/full/restaurant_135621509.jpg",
              "id":"itmx_lua_restaurant",
              "ratings":"4.5",
              "cuisine": "Vietnamese"
           },
           {
              "title":"Thai King",
              "image":"https://upload.wikimedia.org/wikipedia/commons/6/62/Barbieri_-_ViaSophia25668.jpg",
              "id":"itmx_thai_king",
              "ratings":"3.5",
              "cuisine": "Thai"
           },
           {
              "title":"Marubi Ramen",
              "image":"https://b.zmtcdn.com/data/pictures/4/18902194/e92e2a3d4b5c6e25fd4211d06b9a909e.jpg",
              "id":"itmx_marubi_ramen",
              "ratings":"4.0",
              "cuisine": "Japanese"
           },
           {
              "title":"Gong Gan",
              "image":"https://b.zmtcdn.com/data/pictures/3/17871363/c53db6ba261c3e2d4db1afc47ec3eeb0.jpg",
              "id":"itmx_gong_gan",
              "ratings":"3.0",
              "cuisine": "Korean"
           }
        ]"""

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


# action_show_selected_restaurant_details

class ActionShowSelectedRestaurantDetails(Action):
    def name(self) -> Text:
        return "action_show_selected_restaurant_details"


# action_show_booking_summary

class ActionShowBookingSummary(Action):
    def name(self) -> Text:
        return "action_show_booking_summary"


# action_confirm_booking
class ActionConfirmBooking(Action):
    def name(self) -> Text:
        return "action_confirm_booking"

# [
#                 {
#                     "image": "https://b.zmtcdn.com/data/pictures/1/18602861/bd2825ec26c21ebdc945edb7df3b0d99.jpg",
#                     "title": "Taftoon Bar & Kitchen",
#                     "ratings": "4.5",
#                 },
#                 {
#                     "image": "https://b.zmtcdn.com/data/pictures/4/18357374/661d0edd484343c669da600a272e2256.jpg",
#
#                     "ratings": "4.0",
#                     "title": "Veranda"
#                 },
#                 {
#                     "image": "https://b.zmtcdn.com/data/pictures/4/18902194/e92e2a3d4b5c6e25fd4211d06b9a909e.jpg",
#
#                     "ratings": "4.0",
#                     "title": "145 The Mill"
#                 },
#                 {
#                     "image": "https://b.zmtcdn.com/data/pictures/3/17871363/c53db6ba261c3e2d4db1afc47ec3eeb0.jpg",
#
#                     "ratings": "4.0",
#                     "title": "The Fatty Bao"
#                 },
#             ]
