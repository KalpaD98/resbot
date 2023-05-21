from actions.all_actions.common_imports_for_actions import *
from submodules.custom_components.language_detection.language_detector import LanguageDetector

ACTION_DETECT_LANGUAGE = "action_detect_language"
ACTION_SET_PERMANENT_LANGUAGE = "action_set_permanent_language"
ACTION_ASK_LANGUAGE_PREFERENCE = "action_ask_language_preference"


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


class ActionAskLanguagePreference(Action):
    def name(self) -> Text:
        return ACTION_ASK_LANGUAGE_PREFERENCE

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get current language preference from the slot
        current_language = LanguageSelector.get_language(tracker)

        if current_language == EN:
            message = "Language is currently set to english" \
                      "\n\nWould you like to continue in English or switch to Sinhala?"
            options = [
                {
                    TITLE: "Continue in English",
                    PAYLOAD: "/inform_permanent_language{\"language\":\"" + 'en' + "\"}",
                },
                {
                    TITLE: "සිංහලට මාරු වෙන්න",
                    PAYLOAD: "/inform_permanent_language{\"language\":\"" + 'si' + "\"}",
                }
            ]
        elif current_language == SIN:
            message = "භාෂාව දැනට ඉංග්‍රීසි ලෙස සකසා ඇත" \
                      "\n\nඔබ සිංහලෙන් ඉදිරියට යාමට කැමතිද නැතිනම් English භාෂාව සදහා මාරු වීමට කැමතිද?"
            options = [
                {
                    TITLE: "සිංහලෙන් continue කරන්න",
                    PAYLOAD: "/inform_permanent_language{\"language\":\"" + 'si' + "\"}",
                },
                {
                    TITLE: "Change to english",
                    PAYLOAD: "/inform_permanent_language{\"language\":\"" + 'en' + "\"}",
                }
            ]
        else:
            message = "There seems to be an error with your language preference. Please try again later."

        quick_replies = ResponseGenerator.quick_replies(options, with_payload=True)

        dispatcher.utter_message(text=message, quick_replies=quick_replies)

        return []


class ActionSetPermanentLanguage(Action):

    def name(self) -> Text:
        return ACTION_SET_PERMANENT_LANGUAGE

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the language slot
        language = tracker.get_slot('language').lower()

        if language == 'si' or language.contains('si'):
            language = 'si'
            message = "භාෂාව සිංහලට මාරු කරන ලදී."
        else:
            language = 'en'
            message = "ok, lets continue our conversation in English."

        dispatcher.utter_message(text=message)

        # Set the permanent_language slot to the value of language slot
        return [SlotSet('permanent_language', language)]
