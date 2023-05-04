import logging
from typing import List, Dict, Union

from actions.all_actions.helper_functions.response_generator.constants import *


class ResponseGenerator:

    @staticmethod
    def quick_replies(quick_replies_list: List[Union[str, Dict[str, str]]], with_payload: bool = False) -> List[
        Dict[str, str]]:
        """
        Generate quick replies for the chat widget.

        :param quick_replies_list: List of quick reply strings or dictionaries containing title and payload
        :param with_payload: If True, quick_replies_list should contain dictionaries with title and payload
        :return: List of quick reply dictionaries containing title and payload
        """
        quick_reply_text_icons = []

        for quick_reply in quick_replies_list:
            if with_payload:
                quick_reply_text_icons.append(
                    {TITLE: quick_reply.get(TITLE), PAYLOAD: quick_reply.get(PAYLOAD)})
            else:
                quick_reply_text_icons.append({TITLE: quick_reply, PAYLOAD: quick_reply})

        return quick_reply_text_icons

    @staticmethod
    def card_options_carousal(carousal_objects: List[Dict[str, Union[str, List[Dict[str, str]]]]]) -> Dict[
        str, Union[str, Dict[str, Union[str, List[Dict[str, str]]]]]]:
        """
        Generate an options carousel for the chat widget.

        :param carousal_objects: List of carousel object dictionaries
        :return: Carousel dictionary containing carousel elements
        """
        logging.info("Utils [responseGenerator]:  reformation the responses")

        elements_list = []
        carousel = COMPONENT_CAROUSAL

        for carousal_object in carousal_objects:
            card = {DEFAULT_ACTION: carousal_object[DEFAULT_ACTION],
                    IMAGE_URL: carousal_object.get(IMAGE_URL),
                    TITLE: carousal_object.get(TITLE),
                    SUBTITLE: carousal_object.get(SUBTITLE)}

            buttons_list = carousal_object.get(BUTTONS)

            card[BUTTONS] = buttons_list
            elements_list.append(card)

        carousel[PAYLOAD][ELEMENTS] = elements_list

        return carousel

    @staticmethod
    def quick_reply_yes_no_with_payload() -> List[Dict[str, str]]:
        """
        Generate quick replies for the chat widget with yes and no options.

        :return: List of quick reply dictionaries containing title and payload
        """
        quick_replies_with_payload = []

        quick_reply_yes = {
            TITLE: "Yes",
            PAYLOAD: "/affirm"}

        quick_reply_no = {
            TITLE: "No",
            PAYLOAD: "/deny"}

        quick_replies_with_payload.append(quick_reply_yes)
        quick_replies_with_payload.append(quick_reply_no)

        return ResponseGenerator.quick_replies(quick_replies_with_payload, with_payload=True)

    @staticmethod
    def language_related_response_selection(language: str = "en",
                                            english_text: str = "",
                                            english_quick_replies: list = None,
                                            sinhala_text: str = "",
                                            sinhala_quick_replies: list = None) -> tuple:
        """
        Select the language related response.

        :param language: Language of the user. Default is 'en'.
        :param english_text: English text. Default is an empty string.
        :param english_quick_replies: English quick replies. Default is None.
        :param sinhala_text: Sinhala text. Default is an empty string.
        :param sinhala_quick_replies: Sinhala quick replies. Default is None.
        :return: English text, English quick replies, Sinhala text, Sinhala quick replies
        """
        if language == "sin":
            return sinhala_text, sinhala_quick_replies
        else:
            return english_text, english_quick_replies
