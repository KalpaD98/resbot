# Actions.py This files contains custom actions which can be used to run custom Python code.
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import json
import logging
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase

from actions.submodules.constants import *
from actions.submodules.constants import TITLE, SUBCOMPONENT_BUTTON_PAYLOAD
from actions.submodules.mock_data import *
from actions.submodules.response_generator import ResponseGenerator


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ----------------------------------------------- Restaurant Actions ------------------------------------------------ #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# action to show top cuisines based on user preferences.
# This will be shown as a quick reply.
class ActionShowCuisines(Action):
    def name(self) -> Text:
        return "action_show_cuisines"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # get top 10 personalised cuisines for a particular user from the recommendation engine or most popular
        # (frequent)
        cuisines = ['Any', 'Italian', 'Mexican', 'Vietnamese', 'Thai', 'Japanese', 'Korean']

        # generate synonyms for 'Any' cuisine
        # Add payload to quick replies
        cuisines_with_entity_payload = []
        for cuisine in cuisines:
            cuisines_with_entity_payload.append({TITLE: cuisine, PAYLOAD: cuisine})

        # Generate quick replies with Response Generator
        quick_replies_cuisines = ResponseGenerator.quick_replies(cuisines_with_entity_payload, with_payload=True)

        dispatcher.utter_message(text="Please choose a cuisine", quick_replies=quick_replies_cuisines)

        return []

        # this is for vanilla JS UI
        # data = [{"title": cuisine, "payload": cuisine + "_payload"} for cuisine in cuisines]

        # # This is working for normal UI
        # message = {"payload": "quickReplies", "data": data}


# action to show top restaurants based on user preferences and the given cuisine (or without specific cuisine).
class ActionShowRestaurants(Action):

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
        return "action_show_restaurants"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print('\n----------------------Slots-----------------------------------')
        logging.info(tracker.slots)
        print('--------------------------------------------------------------------\n')

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

        rest_list = json.loads(restaurants)

        # Generate restaurant cards with Response Generator
        carousal_objects = []

        # Add data to the carousel card
        for restaurant in rest_list:
            carousal_object = SUBCOMPONENT_CARD.copy()
            carousal_object[TITLE] = restaurant.get(NAME)
            carousal_object[IMAGE_URL] = restaurant.get(IMAGE_URL)
            carousal_object[SUBTITLE] = restaurant.get(CUISINE) + " |  ⭐️ " + str(restaurant.get(RATINGS))

            default_action_payload = SUBCOMPONENT_DEFAULT_ACTION_PAYLOAD.copy()
            default_action_payload[PAYLOAD] = restaurant.get(ID)  # determine a default action for the card later

            buttons = []

            button1 = SUBCOMPONENT_BUTTON_URL.copy()
            button1[TITLE] = "Check Menu"
            button1[URL] = restaurant.get(MENU_URL)  # later replace this with restaurant menu url

            button2 = SUBCOMPONENT_BUTTON_PAYLOAD.copy()
            button2[TITLE] = "Book Table"
            button2[PAYLOAD] = "book" + restaurant.get(ID)
            # book table intent has not been added yet, example: book rtid_s3wjdsud3, book restaurant rtid_s3wjdsud3

            button3 = SUBCOMPONENT_BUTTON_PAYLOAD.copy()
            button3[TITLE] = "View Details"
            button3[PAYLOAD] = "view details " + restaurant.get(ID)

            buttons.append(button1)
            buttons.append(button3)
            buttons.append(button2)

            carousal_object[BUTTONS] = buttons
            carousal_object[DEFAULT_ACTION] = ""  # set to null for temporary debugging
            # carousal_object[DEFAULT_ACTION] = default_action_payload # add a title for def action if possible
            carousal_objects.append(carousal_object)

        dispatcher.utter_message(text="Here are some " + cuisine.lower() + " restaurants I found:",
                                 attachment=ResponseGenerator.card_options_carousal(carousal_objects))

        return []


# TODO: action_request_more_restaurant_options.
# This function is used to pull more restaurant options for the user if they request for more.
class ActionRequestMoreRestaurantOptions(Action):

    def name(self) -> Text:
        return "action_request_more_restaurant_options"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # print slots
        print('\n----------------------Slots-----------------------------------')
        logging.info(tracker.slots)
        print('--------------------------------------------------------------------\n')

        # get more restaurants from the knowledge base that are not in the list of restaurants (remove if exists)
        # already shown to the user

        # if there are more restaurants, send them to the user

        # else send a message to the user saying that there are no more restaurants
        dispatcher.utter_message(text="Sorry, I did not find any more restaurants. "
                                      "Please try again with a different "
                                      "cuisine.")

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
        print('\n----------------------Slots-----------------------------------')
        logging.info(tracker.slots)
        print('--------------------------------------------------------------------\n')

        # get the restaurant id from the tracker
        restaurant_id = tracker.get_slot("restaurant_id")

        if restaurant_id is None:
            logging.info("Restaurant ID not set")

        # get the restaurant data from the knowledge base
        # for now getting from mock data

        # restaurant = await self.knowledge_base.get_object("restaurant", restaurant_id)

        # create a message to show the restaurant details
        # message = "Here are some details about the restaurant: \n"
        # message += "Name: " + restaurant["name"] + "\n"
        # message += "Address: " + restaurant["address"] + "\n"
        # message += "Open: " + restaurant["open"] + "\n"
        # message += "Close: " + restaurant["close"] + "\n"
        # message += "Description: " + restaurant["description"] + "\n"

        # Send the image to the user
        # dispatcher.utter_message(image=image_path)

        # send the message back to the user
        dispatcher.utter_message(text="Details of " + restaurant_id)
        # add multiple messages for each below
        dispatcher.utter_message(text="<small description>, <address>, <Opening hours [weekend,weekdays]>")
        # TODO: after this bot utters Do you want to book a table?.
        dispatcher.utter_message(
            text="Would like to book a table at <restaurant_name>?",
            quick_replies=ResponseGenerator.quick_replies(["Yes", "No"]))
        return []


# action_select_restaurant_ask_booking_confirmation.
class ActionBookSelectedRestaurant(Action):
    def name(self) -> Text:
        return "action_select_restaurant_ask_booking_confirmation"

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

        # get the restaurant data from the knowledge base
        # restaurant = await self.knowledge_base.get_object("restaurant", restaurant_id)

        # create a message to show the restaurant details
        # message = "Here are some details about the restaurant: \n"
        # message += "Name: " + restaurant["name"] + "\n"
        # message += "Address: " + restaurant["address"] + "\n"
        # message += "Open: " + restaurant["open"] + "\n"
        # message += "Close: " + restaurant["close"] + "\n"
        # message += "Description: " + restaurant["description"] + "\n"

        # Send the image to the user
        # dispatcher.utter_message(image=image_path)

        # send the message back to the user
        dispatcher.utter_message(text="You have selected <Restaurant Name>")
        # add multiple messages for each below
        dispatcher.utter_message(text="<small description>, <address>, <Opening hours [weekend,weekdays]>")
        dispatcher.utter_message(text="Would you like to book a table at <restaurant_name>?")

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
        print('\n----------------------Slots-----------------------------------')
        logging.info(tracker.slots)
        print('--------------------------------------------------------------------\n')

        # get restaurant id from the tracker
        restaurant_id = tracker.get_slot("restaurant_id")

        # get the restaurant data from the knowledge base
        # restaurant = await self.knowledge_base.get_object("restaurant", restaurant_id)

        # get the date from the tracker
        # date = tracker.get_slot("date")

        # send the message to the user
        dispatcher.utter_message(text="Your booking summary is as follows:")
        # generate the booking summary
        # message = "Shall I confirm your booking for " + restaurant["name"] + " located at " + \
        #           restaurant["address"] + "on " + date + " at " + time + "."
        dispatcher.utter_message(text="<Booking summary message here>")

        # ask to confirm the booking
        # dispatch a message asking if the user would like to confirm the booking with quick replies <FIX>

        ResponseGenerator.quick_replies(["Yes", "No"])
        # if yes confirm the booking, save in database and send a message to the user (in next action)
        # TODO: if no -> ask if they would like to book a table of another restaurant or exit
        dispatcher.utter_message(text="Would you like to confirm this booking?",
                                 quick_replies=ResponseGenerator.quick_replies(["Yes", "No"]))
        # "Please choose a cuisine",
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

            # generate the booking summary
            message = "Your booking for restaurant_name" + " located at " + "restaurant address" + \
                      "on " + "<date>" + " at " + "<time>" + " has been confirmed. Thank you for using our service."
            #
            # # generate the booking summary
            # message = "Your booking for " + restaurant["name"] + " located at " + restaurant["address"] + \
            #           "on " + date + " at " + time + " has been confirmed. Thank you for using our service."

            # send the message to the user
            dispatcher.utter_message(text=message)

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
        return "action_query_knowledge_base"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # get details from tracker

        # tracker.get_slot("")
        # tracker.get_slot("cuisine")

        return []

######## Important Commented Code ########

###### Documentation for bot - front web chat ######

# TITLE: The title or text displayed on the button
# TYPE: The type of button, which can be either "web_url" or "postback"
# URL: The URL to open if the button is clicked (only used for "web_url" buttons)
# PAYLOAD: The payload to send back to the server if the button is clicked (only used for "postback" buttons)

# carousel = ResponseGenerator.option_carousal(carousal_objects)

#
#
# carousal = COMPONENT_CAROUSAL
# elements_list = []
#
# for restaurant in rest_list:
#     card = {DEFAULT_ACTION: {TYPE: WEB_URL, URL: restaurant.get(IMAGE_URL)},
#             IMAGE_URL: restaurant.get(IMAGE_URL), TITLE: restaurant.get(NAME),
#             SUBTITLE: restaurant.get(CUISINE)}
#
#     buttons_list = []
#
#     button1 = {}
#     button2 = {}
#
#     button1[URL] = restaurant.get(IMAGE_URL)
#     button1[TITLE] = "VIEW_PAGE"
#     # button1[TYPE] = WEB_URL
#
#     button2[URL] = restaurant.get(IMAGE_URL)
#     button2[TITLE] = "Menu"
#     button2[TYPE] = WEB_URL
#
#     buttons_list.append(button1)
#     buttons_list.append(button2)
#
#     card[BUTTONS] = buttons_list
#
#     elements_list.append(card)
#     # SUBCOMPONENT_CARD[]=restaurant.get()
#     # SUBCOMPONENT_CARD[]=restaurant.get()
#     # SUBCOMPONENT_CARD[]=restaurant.get()
#     # SUBCOMPONENT_CARD[]=restaurant.get()
#
# carousal[PAYLOAD][ELEMENTS] = elements_list
