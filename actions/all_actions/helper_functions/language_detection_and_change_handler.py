from actions.all_actions.helper_functions.response_generator.constants import LANGUAGE


class LanguageSelector:

    @staticmethod
    def get_language(tracker):
        # add additional logic later
        return tracker.get_slot(LANGUAGE)
