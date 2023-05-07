import warnings
from typing import Tuple

import fasttext

from actions.all_actions.common_imports_for_actions import *

ACTION_DETECT_LANGUAGE = "action_detect_language"


class ActionDetectLanguage(Action):

    def name(self) -> Text:
        return ACTION_DETECT_LANGUAGE

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the latest message from the user
        user_message = tracker.latest_message.get('text')

        # Detect the language of the user message
        detected_languages = detect_languages(user_message)

        # Set the language slot based on the detected languages
        language = 'en'  # Default to English
        for lang, prob in detected_languages:
            if lang == 'si':
                language = 'si'
                break

        return [SlotSet(LANGUAGE, language)]


# Suppress the warning message
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    model = fasttext.load_model("lid.176.bin")


def detect_languages(text: str, k: int = 2) -> List[Tuple[str, float]]:
    labels, probs = model.predict(text, k=k)
    detected_languages = [(label[-2:], prob) for label, prob in zip(labels, probs)]
    return detected_languages
