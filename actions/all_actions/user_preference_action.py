from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


# add to main actions.py and import commons
class ActionUpdateFavoriteCuisines(Action):

    def name(self) -> Text:
        return "action_update_favorite_cuisines"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cuisines = tracker.get_slot('cuisine')

        # Update the user's favorite_cuisines list by adding the extracted cuisines
        # You can use the user's id to store and retrieve the favorite_cuisines list from your MongoDB database

        # Send a response to the user
        dispatcher.utter_message(text=f"Great! I have updated your favorite cuisines with: {', '.join(cuisines)}")

        return []
