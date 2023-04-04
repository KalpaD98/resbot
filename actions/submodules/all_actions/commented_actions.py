
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ------------------------------------------------- Commented Code -------------------------------------------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Executes the fallback action and goes back to the previous state of the dialogue
# class ActionDefaultFallback(Action):
#     def name(self) -> Text:
#         return ACTION_DEFAULT_FALLBACK_NAME
#
#     async def run(
#             self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(template="my_custom_fallback_template")
#
#         # Revert user message which led to fallback.
#         return [UserUtteranceReverted()]
