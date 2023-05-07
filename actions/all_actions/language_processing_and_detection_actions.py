from actions.all_actions.common_imports_for_actions import *
from submodules.custom_components.language_detector import LanguageDetector

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
        detected_languages = LanguageDetector.detect_languages(user_message)

        # Set the language slot based on the detected languages
        language = 'en'  # Default to English
        for lang, prob in detected_languages:
            if lang == 'si':
                language = 'si'
                break

        return [SlotSet(LANGUAGE, language)]
