from actions.all_actions.common_imports_for_actions import *

# constants
ACTION_ASK_INTENT_CONFIRMATION = "action_ask_intent_confirmation"
ACTION_EXECUTE_CONFIRMED_INTENT = "action_execute_confirmed_intent"


class ActionAskIntentConfirm(Action):
    def name(self) -> Text:
        return ACTION_ASK_INTENT_CONFIRMATION

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO: ask for confirmation by user
        intent_to_confirm = tracker.latest_message['intent']['name']

        return [SlotSet("intent_to_confirm", intent_to_confirm)]


class ActionExecuteConfirmedIntent(Action):
    def name(self) -> Text:
        return ACTION_EXECUTE_CONFIRMED_INTENT

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO: confirm by setting entity / setting slot
        intent_to_confirm = tracker.get_slot("intent_to_confirm")
        # Replace with the code to execute the confirmed intent
        # ...
        return []
