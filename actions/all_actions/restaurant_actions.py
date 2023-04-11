from actions.all_actions.common_imports_for_actions import *

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
        cuisines = restaurant_repo.get_unique_cuisines()

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

        return [SlotSet("restaurant_offset", 0)]


# action to show top restaurants based on user preferences and the given cuisine (or without specific cuisine).
class ActionShowRestaurants(Action):

    def name(self) -> Text:
        return ACTION_SHOW_RESTAURANTS

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get cuisine from the tracker
        cuisine = tracker.get_slot(CUISINE)

        # if cuisine is 'Any Cuisine' then don't filter by cuisine
        # using synonyms for any cuisine unify its value to 'any cuisine'

        # if cuisine is null ask if user wants to filter by cuisine
        if cuisine is None:
            return [FollowupAction(ACTION_SHOW_CUISINES)]
        else:
            logging.info("Cuisine: " + cuisine)

        # send http request to recommendation engine to get top 10 restaurants for the user

        if (cuisine == 'any cuisine') or cuisine is None:
            text_msg = f"I've found some great restaurants for you to try out!"
            restaurants_list = restaurant_repo.get_all_restaurants(limit=10)
        else:
            text_msg = f"I've found some great {cuisine.lower()} restaurants for you to try out!"
            # Get the restaurant list from the database into an array
            restaurants_list = restaurant_repo.get_all_restaurants(limit=10)
            # TODO : uncomment get restaurants by cuisine
            # restaurants_list = restaurant_repo.get_restaurants_by_cuisine(cuisine, limit=10)

        dispatcher.utter_message(text=text_msg,
                                 attachment=ResponseGenerator.card_options_carousal(
                                     RestaurantResponseGenerator.restaurant_list_to_carousal_object(restaurants_list)))
        quick_reply_request_more_restaurant = []

        quick_reply = {
            TITLE: "Show more restaurants",
            PAYLOAD: "/request_more_restaurant_options"}

        quick_reply_request_more_restaurant.append(quick_reply)

        dispatcher.utter_message(
            quick_replies=ResponseGenerator.quick_replies(quick_reply_request_more_restaurant, True))

        return []


# TODO: action_request_more_restaurant_options.
# This function is used to pull more restaurant options for the user if they request for more.
class ActionRequestMoreRestaurantOptions(Action):

    def name(self) -> Text:
        return ACTION_SHOW_MORE_RESTAURANT_OPTIONS

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global restaurant_list
        print_all_slots(tracker)

        # Get the current offset from the slot
        current_offset = tracker.get_slot("restaurant_offset")

        # Increase the offset by 10 (or the limit you're using)
        new_offset = current_offset + 10

        # Get the cuisine from the tracker
        cuisine = tracker.get_slot("cuisine")

        # Fetch the next set of restaurants using the new offset
        if (cuisine == 'any cuisine') or cuisine is None:
            restaurant_list = restaurant_repo.get_all_restaurants(limit=10, offset=new_offset)
        else:
            restaurants_list = restaurant_repo.get_all_restaurants(limit=10, offset=new_offset)
            # TODO : uncomment get restaurants by cuisine
            # restaurant_list = restaurant_repo.get_restaurants_by_cuisine(cuisine, limit=10, offset=new_offset)

        # Check if any more restaurants were found
        if restaurant_list:
            dispatcher.utter_message(text="Here are some more restaurants I found",
                                     attachment=ResponseGenerator.card_options_carousal(
                                         RestaurantResponseGenerator.restaurant_list_to_carousal_object(
                                             restaurant_list)))
        else:
            dispatcher.utter_message(text="Sorry, I did not find any more restaurants.")

        # Update the restaurant_offset slot with the new offset value
        return [SlotSet("restaurant_offset", new_offset)]

# Action search restaurants
# Action search more restaurants
