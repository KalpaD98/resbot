from actions.all_actions.common_imports_for_actions import *

ACTION_SEARCH_AND_SHOW_RESTAURANTS = "action_search_and_show_restaurants"
ACTION_CONFIRM_SEARCH_PARAMETERS = "action_confirm_search_parameters"


class ActionSearchAndShowRestaurants(Action):

    # TODO: implement this PROPERLY

    def name(self) -> Text:
        return ACTION_SEARCH_AND_SHOW_RESTAURANTS

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Get properties from the tracker
            restaurant_name = tracker.get_slot(RESTAURANT_NAME)
            cuisine = tracker.get_slot(CUISINE)
            food_type = tracker.get_slot(FOOD_TYPE)
            state = tracker.get_slot(STATE)
            city = tracker.get_slot(CITY)
            language = tracker.get_slot(LANGUAGE)

            # Send http request to recommendation engine or query database to get restaurants based on properties
            restaurants_list = restaurant_repo.search_restaurants(
                restaurant_name=restaurant_name,
                cuisine=cuisine,
                food_type=food_type,
                state=state,
                city=city,
                limit=10
            )

            if len(restaurants_list) == 0:
                message = "No restaurants found matching your criteria. \n\n" + \
                          "Please try again with different search parameters."
                if language == SIN:
                    message = "ඔබගේ සෙවුම් අනුව restaurants නැත. \n\n" + \
                              "කරුණාකර වෙනත් සෙවුම්මක් කිරීමට උත්සාහ කරන්න."
                dispatcher.utter_message(text=message)
                # have a follow-up action to change the parameters
                return []

            text_msg = "I've found some restaurants based on your search criteria:"
            if language == SIN:
                text_msg = "ඔබගේ සෙවුම් අනුව මෙම restaurants සොයාගත්තේය:"
            dispatcher.utter_message(
                text=text_msg,
                attachment=ResponseGenerator.card_options_carousal(
                    RestaurantResponseGenerator.restaurant_list_to_carousal_object(restaurants_list)))

            return [SlotSet("restaurant_offset", 0)]

        except Exception as e:
            logging.error(f"Error in ActionSearchAndShowRestaurants: {e}")
            dispatcher.utter_message(text="Something went wrong. Please try again later.")

        return [SlotSet("restaurant_offset", 0)]


'''
Remember to add the corresponding slot names like RESTAURANT_NAME, CUISINE, FOOD_TYPE, STATE, and 
CITY at the beginning of the script.

In this action, I've assumed that you have a search_restaurants method in your restaurant_repo that 
in the given properties and returns a list of restaurants matching the search criteria. If you haven't 
implemented this method yet, you'll need to add it to your restaurant_repo.
'''


class ActionConfirmSearchParameters(Action):

    def name(self) -> Text:
        return ACTION_CONFIRM_SEARCH_PARAMETERS

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Get properties from the tracker
            restaurant_name = tracker.get_slot(RESTAURANT_NAME)
            cuisine = tracker.get_slot(CUISINE)
            food_type = tracker.get_slot(FOOD_TYPE)
            state = tracker.get_slot(STATE)
            city = tracker.get_slot(CITY)
            language = tracker.get_slot(LANGUAGE)

            search_parameters = [
                f"Restaurant Name: {restaurant_name}",
                f"Cuisine: {cuisine}",
                f"Food Type: {food_type}",
                f"State: {state}",
                f"City: {city}"
            ]

            search_parameters_text = "\n".join(search_parameters)

            text_msg = f"Here are the search parameters you've entered:\n\n{search_parameters_text}\n\n" \
                       f"Do you want to search for restaurants with these parameters?"

            # TODO : add sinhala language support

            dispatcher.utter_message(text=text_msg,
                                     quick_replies=ResponseGenerator.quick_reply_yes_no_with_payload())

            return []

        except Exception as e:
            logging.error(f"Error in ActionConfirmSearchParameters: {e}")
            dispatcher.utter_message(text="Something went wrong. Please try again later.")

        return []


'''Above action displays the parameters and their values to the user and asks for confirmation using 
the quick_reply_yes_no_with_payload method from the ResponseGenerator class.'''
