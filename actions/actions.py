# This files contains  custom actions which can be used to run custom Python code.

# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.endpoint import HTTPResponse
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
import asyncio
import json


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


class ActionMyKB(ActionQueryKnowledgeBase):
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
        return "action_query_knowledge_base"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # hard coded rest data
        restaurants = """
        [ {
              "title":"Taco Bell",
              "image":"https://b.zmtcdn.com/data/pictures/1/18602861/bd2825ec26c21ebdc945edb7df3b0d99.jpg",
              "ratings":"4.5"
           },
           {
              "title":"Danke",
              "image":"https://lh3.googleusercontent.com/p/AF1QipOs5oyEh2eqR1wHmLuL7WPvdkiqPjyJJdHEeCyI=w600-h0",
              "ratings":"5.0"
           },
           {
              "id":2,
              "title":"I due forni",
              "image":"https://b.zmtcdn.com/data/pictures/4/18357374/661d0edd484343c669da600a272e2256.jpg",
              "ratings":"4"
           },
           {
              "title":"Lụa Restaurant",
              "image":"https://www.collinsdictionary.com/images/full/restaurant_135621509.jpg",
              "ratings":"4.5"
           },
           {
              "title":"Thai King",
              "image":"https://upload.wikimedia.org/wikipedia/commons/6/62/Barbieri_-_ViaSophia25668.jpg",
              "ratings":"3.5"
           },
           {
              "title":"Marubi Ramen",
              "image":"https://b.zmtcdn.com/data/pictures/4/18902194/e92e2a3d4b5c6e25fd4211d06b9a909e.jpg",
              "ratings":"4.0"
           },
           {
              "title":"Gong Gan",
              "image":"https://b.zmtcdn.com/data/pictures/3/17871363/c53db6ba261c3e2d4db1afc47ec3eeb0.jpg",
              "ratings":"3.0"
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
