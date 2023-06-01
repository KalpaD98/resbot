import copy
import time

from rasa.core.actions import action
from rasa.core.actions.loops import LoopAction
from rasa.core.channels import OutputChannel
from rasa.core.nlg import NaturalLanguageGenerator
from rasa.shared.constants import DEFAULT_NLU_FALLBACK_INTENT_NAME
from rasa.shared.core.constants import (
    USER_INTENT_OUT_OF_SCOPE,
    ACTION_LISTEN_NAME,
    ACTION_DEFAULT_FALLBACK_NAME,
    ACTION_DEFAULT_ASK_REPHRASE_NAME,
)
from rasa.shared.core.domain import Domain
from rasa.shared.core.events import (
    Event,
    UserUtteranceReverted,
    ActionExecuted,
    UserUttered,
    ActiveLoop,
)
from rasa.shared.core.trackers import DialogueStateTracker, EventVerbosity
from rasa.shared.nlu.constants import INTENT, PREDICTED_CONFIDENCE_KEY
from rasa.utils.endpoints import EndpointConfig

from actions.all_actions.common_imports_for_actions import *

ACTION_ENHANCED_TWO_STAGE_FALLBACK_NAME = "action_enhanced_two_stage_fallback"


class TwoStageFallbackAction(LoopAction):
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
