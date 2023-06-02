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

ACTION_ENHANCED_TWO_STAGE_FALLBACK_NAME = "action_enhanced_two_stage_fallback"

