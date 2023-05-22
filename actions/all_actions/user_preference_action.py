from actions.all_actions.common_imports_for_actions import *


class ActionUpdateFavoriteCuisines(Action):

    def name(self) -> Text:
        return "action_update_favorite_cuisines"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cuisines = tracker.get_slot('cuisine')

        # Update the user's favorite_cuisines list by adding the extracted cuisines
        # You can use the user's id to store and retrieve the favorite_cuisines list from your MongoDB database

        language = LanguageSelector.get_language(tracker)

        # Send a response to the user
        message = f"Great! I have updated your favorite cuisines with: {', '.join(cuisines)}"
        if language == SIN:
            message = f" ඔබගේ ප්‍රියතම cusines යාවත්කාලීන කරන ලදී: {', '.join(cuisines)}"

        dispatcher.utter_message(text=message)

        return []
