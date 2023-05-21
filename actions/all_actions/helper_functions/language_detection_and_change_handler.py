from actions.all_actions.helper_functions.response_generator.constants import LANGUAGE


class LanguageSelector:

    @staticmethod
    def get_language(tracker):
        # Check if permanent_language slot exists and is not None
        permanent_language = tracker.get_slot('permanent_language')
        if permanent_language:
            return permanent_language

        # If permanent_language slot doesn't exist or is None, return the language slot
        else:
            return tracker.get_slot(LANGUAGE)
