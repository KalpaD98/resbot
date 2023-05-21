from actions.all_actions.common_imports_for_actions import *

# Constants
ACTION_SHOW_CUISINES = "action_show_cuisines"
ACTION_SHOW_RESTAURANTS = "action_show_restaurants"
ACTION_SHOW_MORE_RESTAURANT_OPTIONS = "action_show_more_restaurant_options"


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ----------------------------------------------- Restaurant Actions ------------------------------------------------ #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# action to show top cuisines based on user preferences.
class ActionShowCuisines(Action):
    def name(self) -> Text:
        return ACTION_SHOW_CUISINES

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
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
            language = LanguageSelector.get_language(tracker)

            message = "Choose or type a cuisine"
            if language == SIN:
                message = "ආහාර පිසීමක් (cuisine) එකක් තෝරන්න හෝ type කරන්න"

            dispatcher.utter_message(text=message, quick_replies=quick_replies_cuisines)

        except Exception as e:
            logging.error(f"Error in ActionShowCuisines: {e}")
            dispatcher.utter_message(text="Something went wrong. Please try again later.")

        return []


# action to show top restaurants based on user preferences and the given cuisine (or without specific cuisine).
class ActionShowRestaurants(Action):

    def name(self) -> Text:
        return ACTION_SHOW_RESTAURANTS

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # get cuisine from the tracker
            cuisine = tracker.get_slot(CUISINE).lower()

            # if cuisine is null ask if user wants to filter by cuisine
            if cuisine is None:
                return [FollowupAction(ACTION_SHOW_CUISINES)]
            else:
                logging.info("Cuisine: " + cuisine)

            # send http request to recommendation engine to get top 10 restaurants for the user

            language = LanguageSelector.get_language(tracker)
            restaurants_list = []

            if cuisine is None or 'any' in cuisine or 'whatever' in cuisine:
                message = "I've found some great restaurants for you to try out!"
                if language == SIN:
                    message = "ඔබට try කර බැලීම සදහා විශිෂ්ට අවන්හල් කිහිපයක්!"
                restaurants_list = restaurant_repo.get_all_restaurants(limit=10)
            else:
                message = f"I've found some great {cuisine.lower()} restaurants for you to try out!"
                if language == SIN:
                    message = f"ඔබට try කර බැලීම සදහා විශිෂ්ට {cuisine.lower()} අවන්හල් කිහිපයක්!"
                restaurants_list = restaurant_repo.get_restaurants_filter_by_cuisine(cuisine, limit=10)

            if len(restaurants_list) == 0:
                message = f"Sorry, I couldn't find {cuisine} restaurants for you to try out!"
                if language == SIN:
                    message = f"කණගාටුයි, {cuisine} අවන්හල් හමු නොවීය!"

                dispatcher.utter_message(text=message)
                return [SlotSet("restaurant_offset", 0), FollowupAction(ACTION_SHOW_CUISINES)]

            dispatcher.utter_message(text=message,
                                     attachment=ResponseGenerator.card_options_carousal(
                                         RestaurantResponseGenerator.
                                         restaurant_list_to_carousal_object(restaurants_list)))
            # consider adding view more option
            return [SlotSet("restaurant_offset", 0)]

        except Exception as e:
            logging.error(f"Error in ActionShowRestaurants: {e}")
            dispatcher.utter_message(text="Something went wrong. Please try again later.")

        return [SlotSet("restaurant_offset", 0)]


# TODO: action_request_more_restaurant_options.
# This function is used to pull more restaurant options for the user if they request for more.
class ActionRequestMoreRestaurantOptions(Action):

    def name(self) -> Text:
        return ACTION_SHOW_MORE_RESTAURANT_OPTIONS

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
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
                restaurant_list = restaurant_repo.get_restaurants_filter_by_cuisine(cuisine, limit=10,
                                                                                    offset=new_offset)
            language = LanguageSelector.get_language(tracker)

            message = "Here are some more restaurants I found"
            if language == SIN:
                message = "තවත් ආපනශාලා කිහිපයක් මෙන්න"

            # Check if any more restaurants were found
            if restaurant_list:
                dispatcher.utter_message(text=message,
                                         attachment=ResponseGenerator.card_options_carousal(
                                             RestaurantResponseGenerator.restaurant_list_to_carousal_object(
                                                 restaurant_list)))
            else:
                message = "Sorry, I did not find any more restaurants."
                if language == SIN:
                    message = "කණගාටුයි, මට තවත් restaurants කිසිවක් සොයා ගත නොහැකි විය."
                dispatcher.utter_message(text=message)

            # Update the restaurant_offset slot with the new offset value
            return [SlotSet("restaurant_offset", new_offset)]

        except Exception as e:

            logging.error(f"Error in ActionRequestMoreRestaurantOptions: {e}")
            dispatcher.utter_message(text="Something went wrong. Please try again later.")

        return [SlotSet("restaurant_offset", 0)]

# Action search restaurants
# Action search more restaurants
