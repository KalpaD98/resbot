# Actions.py This files contains custom all_actions which can be used to run custom Python code.
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

# noinspection PyUnresolvedReferences
from actions.all_actions.bot_response_actions import *  # bot response actions
# noinspection PyUnresolvedReferences
from actions.all_actions.fallback_actions import *  # fallback  actions
# ------ All other actions ------
# noinspection PyUnresolvedReferences
from actions.all_actions.form_validation_actions import *  # form validation actions
# noinspection PyUnresolvedReferences
from actions.all_actions.knowledge_base_actions import *  # knowledge base actions
# noinspection PyUnresolvedReferences
from actions.all_actions.restaurant_actions import *  # restaurant actions
# noinspection PyUnresolvedReferences
from actions.all_actions.restaurant_booking_actions import *  # restaurant booking actions
# noinspection PyUnresolvedReferences
from actions.all_actions.restaurant_booking_cancel_actions import *  # restaurant booking delete
# noinspection PyUnresolvedReferences
from actions.all_actions.restaurant_booking_carousal_actions import *  # restaurant booking read
# noinspection PyUnresolvedReferences
from actions.all_actions.restaurant_booking_change_actions import *  # restaurant booking update
# noinspection PyUnresolvedReferences
from actions.all_actions.restaurant_search_actions import *  # restaurant search actions
# noinspection PyUnresolvedReferences
from actions.all_actions.slot_validation_actions import *  # slot validation actions
# User related actions
# noinspection PyUnresolvedReferences
from actions.all_actions.user_actions import *  # user actions
# noinspection PyUnresolvedReferences
from actions.all_actions.user_preference_action import *  # user preference actions

# CONSTANTS
ACTION_ASK_ANYTHING_ELSE = "action_ask_anything_else"
ACTION_ASK_WHAT_USER_WANTS = "action_ask_what_user_wants"
ACTION_DEFAULT_FALLBACK = "action_default_fallback"
ACTION_ENHANCED_TWO_STAGE_FALLBACK_NAME = "action_enhanced_two_stage_fallback"
ACTION_CLEAR_RESTAURANT_BOOKING_SLOTS = "action_clear_restaurant_booking_slots"


class ActionAnythingElse(Action):
    def name(self) -> Text:
        return ACTION_ASK_ANYTHING_ELSE

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_text = "Is there anything else I can help you with?"
        sinhala_text = "ඔබට උදව් අවශ්යයි වෙනත් යමක් තිබේද?"

        english_quick_replies_with_payload = [
            # {"title": QR_SEARCH_RESTAURANTS, "payload": "/want_to_search_restaurants"},
            {"title": QR_BROWSE_RESTAURANTS, "payload": "/request_restaurants"},
            {"title": "View bookings", "payload": "/view_bookings"},
            {"title": "No thanks", "payload": "/goodbye"},
        ]

        sinhala_quick_replies_with_payload = [
            # {"title": "ආපනශාලා සොයන්න", "payload": "/want_to_search_restaurants"},
            {"title": "ආපනශාලා පෙන්වන්න", "payload": "/request_restaurants"},
            {"title": "Bookings පෙන්වන්න", "payload": "/view_bookings"},
            {"title": "නැත ස්තුතියි", "payload": "/goodbye"},
        ]

        final_text, final_quick_replies_with_payload = \
            ResponseGenerator.language_related_response_selection(
                LanguageSelector.get_language(tracker),
                english_text,
                english_quick_replies_with_payload,
                sinhala_text,
                sinhala_quick_replies_with_payload)

        dispatcher.utter_message(text=final_text,
                                 quick_replies=ResponseGenerator.quick_replies(final_quick_replies_with_payload, True))
        return []


# anything else with quick replies
class ActionAskWhatUserWants(Action):
    def name(self) -> Text:
        return ACTION_ASK_WHAT_USER_WANTS

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_text = "What do you want to do?"
        sinhala_text = "ඔබට අවශ්ය සේවාව කුමක් ද?"

        english_quick_replies_with_payload = [
            {
                TITLE: QR_HI,
                PAYLOAD: "/greet"},
            {
                TITLE: QR_BROWSE_RESTAURANTS,
                PAYLOAD: "/request_restaurants"},
            # {
            #     TITLE: QR_SEARCH_RESTAURANTS,
            #     PAYLOAD: "/want_to_search_restaurants"}
        ]

        sinhala_quick_replies_with_payload = [
            {
                TITLE: QR_HI,
                PAYLOAD: "/greet"},
            {
                TITLE: "ආපනශාලා පෙන්වන්න",
                PAYLOAD: "/request_restaurants"},
            # {
            #     TITLE: "ආපනශාලා සොයන්න",
            #     PAYLOAD: "/want_to_search_restaurants"}
        ]

        final_text, final_quick_replies_with_payload = \
            ResponseGenerator.language_related_response_selection(
                LanguageSelector.get_language(tracker),
                english_text,
                english_quick_replies_with_payload,
                sinhala_text,
                sinhala_quick_replies_with_payload)

        dispatcher.utter_message(text=final_text,
                                 quick_replies=ResponseGenerator.quick_replies(final_quick_replies_with_payload, True))
        return []


# clear slots related to restaurant booking when user ask to stop booking
class ActionClearRestaurantBookingSlots(Action):
    def name(self) -> Text:
        return ACTION_CLEAR_RESTAURANT_BOOKING_SLOTS

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet(CUISINE, None),
                SlotSet(RESTAURANT_ID, None),
                SlotSet(BOOKING_ID, None),
                SlotSet(SELECTED_RESTAURANT, None),
                SlotSet(NUM_PEOPLE, None),
                SlotSet(DATE, None),
                SlotSet(TIME, None)]


# --------------------------------------------------------------------------------------------- #

class TwoStageFallbackAction(LoopAction, Action):
    def __init__(self, action_endpoint: Optional[EndpointConfig] = None) -> None:
        self._action_endpoint = action_endpoint

    def name(self) -> Text:
        return ACTION_ENHANCED_TWO_STAGE_FALLBACK_NAME

    async def do(
            self,
            output_channel: "OutputChannel",
            nlg: "NaturalLanguageGenerator",
            tracker: "DialogueStateTracker",
            domain: "Domain",
            events_so_far: List[Event],
    ) -> List[Event]:
        if _user_should_affirm(tracker, events_so_far):
            return await self._ask_affirm(output_channel, nlg, tracker, domain)

        return await self._ask_rephrase(output_channel, nlg, tracker, domain)

    async def _ask_affirm(
            self,
            output_channel: OutputChannel,
            nlg: NaturalLanguageGenerator,
            tracker: DialogueStateTracker,
            domain: Domain,
    ) -> List[Event]:

        # Get the intent ranking from the latest message
        intent_ranking = tracker.latest_message['intent_ranking']

        # Select the top 3 intents

        top_intents = intent_ranking[:3]

        # Create buttons for the top 3 intents
        buttons = [{"title": intent["name"], "payload": f"/{intent['name']}"} for intent in top_intents]
        # Add a button for "None of the above"
        buttons.append({"title": "None of the above", "payload": "/out_of_scope"})

        # Create a message with the buttons
        message = {
            "type": "text",
            "text": "I'm not quite sure about what you said, did you mean:",
            "buttons": buttons,
        }

        # Send the message
        await output_channel.send_response(tracker.sender_id, message)

        return []

    async def _ask_rephrase(
            self,
            output_channel: OutputChannel,
            nlg: NaturalLanguageGenerator,
            tracker: DialogueStateTracker,
            domain: Domain,
    ) -> List[Event]:
        rephrase = action.action_for_name_or_text(
            ACTION_DEFAULT_ASK_REPHRASE_NAME, domain, self._action_endpoint
        )

        return await rephrase.run(output_channel, nlg, tracker, domain)

    async def is_done(
            self,
            output_channel: "OutputChannel",
            nlg: "NaturalLanguageGenerator",
            tracker: "DialogueStateTracker",
            domain: "Domain",
            events_so_far: List[Event],
    ) -> bool:
        _user_clarified = _last_intent_name(tracker) not in [
            DEFAULT_NLU_FALLBACK_INTENT_NAME,
            USER_INTENT_OUT_OF_SCOPE,
        ]
        return (
                _user_clarified
                or _two_fallbacks_in_a_row(tracker)
                or _second_affirmation_failed(tracker)
        )

    async def deactivate(
            self,
            output_channel: "OutputChannel",
            nlg: "NaturalLanguageGenerator",
            tracker: "DialogueStateTracker",
            domain: "Domain",
            events_so_far: List[Event],
    ) -> List[Event]:
        if _two_fallbacks_in_a_row(tracker) or _second_affirmation_failed(tracker):
            return await self._give_up(output_channel, nlg, tracker, domain)

        # revert fallback events
        reverted_event: List[Event] = [UserUtteranceReverted()]
        return reverted_event + _message_clarification(tracker)

    async def _give_up(
            self,
            output_channel: OutputChannel,
            nlg: NaturalLanguageGenerator,
            tracker: DialogueStateTracker,
            domain: Domain,
    ) -> List[Event]:
        fallback = action.action_for_name_or_text(
            ACTION_DEFAULT_FALLBACK_NAME, domain, self._action_endpoint
        )

        return await fallback.run(output_channel, nlg, tracker, domain)


def _last_intent_name(tracker: DialogueStateTracker) -> Optional[Text]:
    last_message = tracker.latest_message
    if not last_message:
        return None

    return last_message.intent_name


def _two_fallbacks_in_a_row(tracker: DialogueStateTracker) -> bool:
    return _last_n_intent_names(tracker, 2) == [
        DEFAULT_NLU_FALLBACK_INTENT_NAME,
        DEFAULT_NLU_FALLBACK_INTENT_NAME,
    ]


def _last_n_intent_names(
        tracker: DialogueStateTracker, number_of_last_intent_names: int
) -> List[Optional[Text]]:
    intent_names: List[Optional[Text]] = []
    for i in range(number_of_last_intent_names):
        message = tracker.get_last_event_for(
            (UserUttered, UserUtteranceReverted),
            skip=i,
            event_verbosity=EventVerbosity.AFTER_RESTART,
        )
        if isinstance(message, UserUttered):
            intent_names.append(message.intent.get("name"))

    return intent_names


def _user_should_affirm(
        tracker: DialogueStateTracker, events_so_far: List[Event]
) -> bool:
    fallback_was_just_activated = any(
        isinstance(event, ActiveLoop) for event in events_so_far
    )
    if fallback_was_just_activated:
        return True

    return _last_intent_name(tracker) == DEFAULT_NLU_FALLBACK_INTENT_NAME


def _second_affirmation_failed(tracker: DialogueStateTracker) -> bool:
    return _last_n_intent_names(tracker, 3) == [
        USER_INTENT_OUT_OF_SCOPE,
        DEFAULT_NLU_FALLBACK_INTENT_NAME,
        USER_INTENT_OUT_OF_SCOPE,
    ]


def _message_clarification(tracker: DialogueStateTracker) -> List[Event]:
    latest_message = tracker.latest_message
    if not latest_message:
        raise TypeError(
            "Cannot issue message clarification because "
            "latest message is not on tracker."
        )

    clarification = copy.deepcopy(latest_message)
    clarification.parse_data[INTENT][PREDICTED_CONFIDENCE_KEY] = 1.0  # type: ignore[literal-required]  # noqa E501
    clarification.timestamp = time.time()
    return [ActionExecuted(ACTION_LISTEN_NAME), clarification]

# class ActionDefaultFallback(Action):
#     def name(self) -> Text:
#         return "action_default_fallback"
#
#     def run(
#             self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#         # get the list of intents from the latest user message
#         intents = [intent['name'] for intent in tracker.latest_message['intent_ranking']]
#
#         # generate a message with a list of buttons for user to select
#         buttons = [{"title": intent, "payload": f"/{intent}"} for intent in intents]
#
#         dispatcher.utter_message(
#             text="I'm not sure about that. Did you mean one of these?",
#             buttons=buttons,
#         )
#
#         return [UserUtteranceReverted(), FollowupAction("action_listen")]


# class ActionDefaultFallback(Action):
#     """Executes the fallback action and
#     goes back to the previous state
#     of the dialogue"""
#
#     def name(self) -> Text:
#         return ACTION_DEFAULT_FALLBACK
#
#     async def run(
#             self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#         language = LanguageSelector.get_language(tracker)
#         if language == SIN:
#             dispatcher.utter_message(template="my_custom_fallback_template_sin")
#         else:
#             dispatcher.utter_message(template="my_custom_fallback_template")
#
#         # Revert user message which led to fallback.
#         return [UserUtteranceReverted()]
