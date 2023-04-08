from actions.all_actions.common_imports_for_actions import *

# from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase

# CONSTANTS
ACTION_QUERY_KNOWLEDGE_BASE = "action_query_knowledge_base"


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# --------------------------------------------- Knowledge Base Actions ---------------------------------------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# action to show top restaurants based on user preferences and the given cuisine (or without specific cuisine).
class ActionQueryKnowledgeBase(Action):

    def __init__(self):
        # load db_knowledge base with data from the given file
        print("knowledge base not connected")

        # # overwrite the representation function of the restaurant object
        # # by default the representation function is just the name of the object
        #
        # kb.set_representation_function_of_object(
        #     "restaurant", lambda obj: obj["name"] + "(" + obj["cuisine"] + ")"
        # )
        #
        # super().__init__(kb)

    def name(self) -> Text:
        return ACTION_QUERY_KNOWLEDGE_BASE

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return []
