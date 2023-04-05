# Actions.py This files contains custom all_actions which can be used to run custom Python code.
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# noinspection PyUnresolvedReferences
from actions.all_actions.form_validation_actions import *
# noinspection PyUnresolvedReferences
from actions.all_actions.knowledge_base_actions import *
# noinspection PyUnresolvedReferences
from actions.all_actions.restaurant_actions import *
# noinspection PyUnresolvedReferences
from actions.all_actions.restaurant_booking_actions import *
# noinspection PyUnresolvedReferences
from actions.all_actions.slot_validation_actions import *
# noinspection PyUnresolvedReferences
from actions.all_actions.user_actions import *


# anything else with quick replies
class ActionAnythingElse(Action):
    def name(self) -> Text:
        return ACTION_ASK_ANYTHING_ELSE

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # quick replies for show more and search with payload
        quick_replies_with_payload = []

        quick_reply_show_more = {
            TITLE: QR_SHOW_MORE_RESTAURANTS,
            PAYLOAD: "/request_more_restaurant_options"}

        quick_reply_no = {
            TITLE: "No thanks",
            PAYLOAD: "/stop"}

        quick_reply_search_restaurant = {
            TITLE: QR_SEARCH_RESTAURANTS,
            PAYLOAD: "/want_to_search_restaurants"}

        quick_replies_with_payload.append(quick_reply_show_more)
        quick_replies_with_payload.append(quick_reply_search_restaurant)
        quick_replies_with_payload.append(quick_reply_no)

        dispatcher.utter_message(text="Is there anything else I can help you with?",
                                 quick_replies=ResponseGenerator.quick_replies(quick_replies_with_payload, True))
        return []

######################################################## backup ########################################################
#
# # noinspection PyUnresolvedReferences
# from actions.all_actions.form_validation_actions import *
# # noinspection PyUnresolvedReferences
# from actions.all_actions.knowledge_base_actions import *
# # noinspection PyUnresolvedReferences
# from actions.all_actions.restaurant_actions import *
# # noinspection PyUnresolvedReferences
# from actions.all_actions.restaurant_booking_actions import *
# # noinspection PyUnresolvedReferences
# from actions.all_actions.slot_validation_actions import *
# # noinspection PyUnresolvedReferences
# from actions.all_actions.user_actions import *
