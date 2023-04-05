from actions.all_actions.common_imports import *

# Constants
ACTION_SHOW_CUISINES = "action_show_cuisines"
ACTION_SHOW_RESTAURANTS = "action_show_restaurants"
ACTION_SHOW_MORE_RESTAURANT_OPTIONS = "action_show_more_restaurant_options"
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
