import random

from actions.all_actions.common_imports_for_actions import *


class ActionUtterGreetAndIntro(Action):
    def name(self) -> Text:
        return "action_utter_greet_and_intro"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        hi_message = random.choice(["Hi!", "Hey!", "Hello!", "Hi 😃 there!", "Hello there 😀"])
        intro_message = random.choice(
            [
                "I'm ResBot! 🍴, I can recommend amazing restaurants and make reservations seamless for you 🌟.",
                "I'm ResBot, your dining assistant. I help find ideal restaurants and make reservations for you 🌟."
            ]
        )

        sinhala_hi_message = random.choice(["හායි! 😃", "හෙලෝ!", "ආයුබෝවන් 😀"])
        sinhala_intro_message = random.choice(
            [
                "මම ResBot! 🍴, මට අවන්හල් නිර්දේශ කළ හැකි අතර ඔබට වෙන් කිරීම් මා හරහා සිදු කළ හැක.",
                "මම ResBot, ඔබේ AI භෝජන සහකාර. මම ඔබට සුදුසු අවන්හල් සොයා ගැනීමට සහ ඔබ වෙනුවෙන් එය වෙන් කරවා ගැනීමට උදවු කරමි 🌟."
            ]
        )

        is_authenticated = tracker.get_slot(IS_AUTHENTICATED)

        if is_authenticated:
            english_messages = hi_message
            sinhala_messages = sinhala_hi_message
        else:
            english_messages = hi_message + "\n\n" + intro_message
            sinhala_messages = sinhala_hi_message + "\n\n" + sinhala_intro_message

        language = LanguageSelector.get_language(tracker)

        if language == SIN:
            dispatcher.utter_message(text=sinhala_messages)
        else:
            dispatcher.utter_message(text=english_messages)

        return []


class ActionUtterWannaBook(Action):
    def name(self) -> Text:
        return "action_utter_wanna_book"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "Would you like to reserve a table at a fantastic restaurant? 🍽️"
        ]
        sinhala_messages = [
            "High quality ආපන ශාලාවක මේසයක් වෙන්කරවා ගැනීමට කැමතිද? 🍽️"
        ]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterPleaseRephrase(Action):
    def name(self) -> Text:
        return "action_utter_please_rephrase"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "I'm sorry, I couldn't understand that. Could you rephrase it?",
            "Sorry I didn't get that. Can you rephrase?",
            "Sorry, I'm not sure I understand. Can you rephrase?"
        ]
        sinhala_messages = [
            "සමාවෙන්න, මට එය තේරුම් ගන්න බැරි විය. වෙනස් වචනයෙන් නැවත කිව හැකිද?",
            "කණගාටුයි, මට තේරුන් නැහැ. වෙනස් වචනයෙන් නැවත කිව හැකිද?"
        ]
        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterGreetAgain(Action):  # not used in any stories
    def name(self) -> Text:
        return "action_utter_greet_again"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Hi there again!", "Hello again!"]
        sinhala_messages = ["නැවතත් ආයුබෝවන්!"]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterMoodGreatFeedback(Action):
    def name(self) -> Text:
        return "action_utter_mood_great_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Cool! 😎", "Nice to hear 😃 that", "Happy to hear 😊"]
        sinhala_messages = ["නියමයි.", "ඔබට උදව් කිරීම සතුටක්."]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterMoodUnhappyFeedback(Action):
    def name(self) -> Text:
        return "action_utter_mood_unhappy_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "Sorry to hear that, maybe having something will make you feel better.",
            "Hmm, eating something might help you feel better."
        ]

        sinhala_messages = [
            "ඔක අමතක වෙන්නත් එක්ක මොනාහරි කමුද?.",
            "hmm, මොනාහරි කෑවනම් ඔක මගහැරෙයි සමහරවිට."
        ]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterEmojiGreatFeedback(Action):
    def name(self) -> Text:
        return "action_utter_emoji_great_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["😊", "😄"]
        sinhala_messages = ["😊", "😄"]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterEmojiMoodUnhappyFeedback(Action):
    def name(self) -> Text:
        return "action_utter_emoji_mood_unhappy_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Eating something might help 🤗", "Eating something might help 😊"]
        sinhala_messages = ["ඔක අමතක වෙන්නත් එක්ක මොනාහරි කමුද?.", "hmm, මොනාහරි කෑවනම් ඔක මගහැරෙයි සමහරවිට."]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterThankYou(Action):
    def name(self) -> Text:
        return "action_utter_thank_you"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "Thank you for using our service. If you need any assistance in the future, feel free to ask."
        ]
        sinhala_messages = [
            "අපගේ සේවාව භාවිතා කලාට ස්තුතියි.  ඔබට කිසියම් සහයක් අවශ්‍ය නම්, නොපසුබටව අසන්න!"
        ]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterWelcome(Action):
    def name(self) -> Text:
        return "action_utter_welcome"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "You're welcome!",
            "No problem!",
            "Happy to help!",
            "My pleasure!",
            "Anytime!",
            "Always happy to help!"
        ]

        sinhala_messages = [
            "ඔක මොකක්ද",
            "මාගෙ ප්‍රනාමයයි"
        ]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterGoodbye(Action):
    def name(self) -> Text:
        return "action_utter_goodbye"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Bye", "Goodbye", "Farewell", "See you later"]

        sinhala_messages = ["ටටා බායි", "නැවත හමුවෙමු"]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterByeSeeYouLater(Action):
    def name(self) -> Text:
        return "action_utter_bye_see_you_later"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Good Bye. See you later!"]
        sinhala_messages = ["ආයුබෝවන්. නැවත හමුවෙමු!"]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterAskUserName(Action):
    def name(self) -> Text:
        return "action_ask_user_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "May I know your name? (first name is sufficient)"
        ]
        sinhala_messages = [
            "මට ඔබගේ නම දැන ගත හැකිද? (පළමු නම ප්‍රමාණවත්)"
        ]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterAskUserEmail(Action):
    def name(self) -> Text:
        return "action_ask_user_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Enter your email address."]
        sinhala_messages = ["ඔබගේ email ලිපිනය ඇතුලත් කරන්න."]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterAskUserPassword(Action):
    def name(self) -> Text:
        return "action_ask_user_password"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Enter password."]
        sinhala_messages = ["මුරපදය ඇතුලත් කරන්න."]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterAskDate(Action):
    def name(self) -> Text:
        return "action_ask_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "When would you like to make the booking? A future date (tomorrow or later) "
            "in the format [YYYY/MM/DD] is preferred",
            "What date do you have in mind for the booking?  A future date (tomorrow or later) "
            "in the format [YYYY/MM/DD] is preferred"
        ]
        sinhala_messages = [
            "ඔබ වෙන්කරවා ගැනීමට කැමති කවදාද? අනාගත දිනයක් (හෙට හෝ පසුව) "
            "[YYYY/MM/DD] ආකෘතියෙන් වඩාත් කැමති වේ"
            ,

            "ඔබට වෙන්කරවා ගැනීම සඳහා ඇති දිනය කුමක්ද? අනාගත දිනයක් (හෙට හෝ පසුව)"
            "[YYYY/MM/DD] ආකෘතියෙන් වඩාත් කැමති වේ"
        ]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterAskNumPeople(Action):
    def name(self) -> Text:
        return "action_ask_num_people"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "May I know the number of people for the booking?",
            "For how many people are you planing to make the reservation?"
        ]
        sinhala_messages = [
            "වෙන්කරවා ගැනීම සඳහා පුද්ගලයින් ගණන මට දැනගත හැකිද?",
            "ඔබ කොපමණ පිරිසක් සඳහා වෙන්කරවා ගැනීමට සැලසුම් කරනවාද?"
        ]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterNoChangesMadeToBooking(Action):
    def name(self) -> Text:
        return "action_utter_no_changes_made_to_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["No changes were made to your booking"]
        sinhala_messages = ["ඔබේ වෙන්කිරීමේ කිසිදු වෙනසක් සිදු කර නොමැත"]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterAskFavoriteCuisines(Action):
    def name(self) -> Text:
        return "action_utter_ask_favorite_cuisines"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "What are your favorite cuisines? You can provide multiple cuisines, like Italian, Chinese, "
            "Indian, or Mexican."]
        sinhala_messages = [
            "ඔබේ ප්‍රියතම ආහාර වර්ග මොනවාද? ඔබට Italian, Chinese, Indian, හෝ Mexican වැනි විවිධ ආහාර වර්ග සැපයිය හැක"
        ]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


# all below have not been used in any stories


class ActionUtterLoginToContinue(Action):  # not used in any story
    def name(self) -> Text:
        return "action_utter_login_to_continue"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Please login to continue."]
        sinhala_messages = ["කරුණාකර ඉදිරියට යාමට log වන්න."]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterAlreadyLoggedIn(Action):  # not used in any story
    def name(self) -> Text:
        return "action_utter_already_logged_in"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["You are already logged in."]
        sinhala_messages = ["ඔබ දැනටමත් ලොගින් වී ඇත."]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterAskCancelAnotherBooking(Action):  # not used in any story
    def name(self) -> Text:
        return "action_utter_ask_cancel_another_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Do you want to cancel another booking?"]
        sinhala_messages = ["ඔබට වෙනත් වෙන් කිරීමක් අවලංගු කිරීමට අවශ්‍යද?"]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterAskNewBookingDate(Action):  # not used in any story
    def name(self) -> Text:
        return "action_utter_ask_new_booking_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["What is the new date for the booking?"]
        sinhala_messages = ["Booking එක සඳහා නව දිනය කුමක්ද?"]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterAskChangeAnotherBooking(Action):  # not used in any story
    def name(self) -> Text:
        return "action_utter_ask_change_another_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Do you want to change another booking?"]
        sinhala_messages = ["ඔබට වෙනත් booking එකක් වෙනස් කිරීමට අවශ්‍යද?"]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterAskTryAgain(Action):  # not used in any story
    def name(self) -> Text:
        return "action_utter_ask_try_again"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "Would you like to try again?",
            "Do you want to try searching again?"
        ]
        sinhala_messages = [
            "ඔබ නැවත උත්සාහ කිරීමට කැමතිද?",
            "ඔබට නැවත සෙවීමට උත්සාහ කිරීමට අවශ්‍යද?"
        ]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterAskDifferentDate(Action):  # not used in any story
    def name(self) -> Text:
        return "action_utter_ask_different_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "Would you like to select a different date for the booking?",
            "Do you want to choose another date for the reservation?"
        ]
        sinhala_messages = [
            "ඔබ booking එක සඳහා වෙනත් දිනයක් තෝරා ගැනීමට කැමතිද?",
            "ඔබට booking එක සඳහා වෙනත් දිනයක් තෝරා ගැනීමට අවශ්‍යද?"
        ]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterAskDifferentRestaurant(Action):  # not used in any story
    def name(self) -> Text:
        return "action_utter_ask_different_restaurant"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "Would you like to choose a different restaurant?",
            "Do you want to look for another restaurant?"
        ]
        sinhala_messages = [
            "ඔබ වෙනත් අවන්හලක් තෝරා ගැනීමට කැමතිද?",
            "ඔබට වෙනත් අවන්හලක් සොයා ගැනීමට අවශ්‍යද?"
        ]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterBookingConfirmation(Action):  # not used in any story
    def name(self) -> Text:
        return "action_utter_booking_confirmation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        restaurant = tracker.get_slot("restaurant")
        booking_date = tracker.get_slot("date")
        num_people = tracker.get_slot("num_people")

        english_messages = [
            f"Your booking at {restaurant['name']} on {booking_date} for {num_people} people has been confirmed.",
            f"Congratulations! Your reservation at {restaurant['name']} for {num_people} people on {booking_date} "
            f"is confirmed."
        ]
        sinhala_messages = [
            f"පුද්ගලයින් {num_people} ක් සඳහා {booking_date} දින {restaurant['name']} ඔබේ booking එක තහවුරු කළෙමි.",

            f"සුබ පැතුම්! {booking_date} දින {num_people} දෙනෙකු සඳහා {restaurant['name']} හි ඔබගේ booking එක"
            f"තහවුරු කළෙමි."
        ]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterProcessingTheRequest(Action):  # not used in any story
    def name(self) -> Text:
        return "action_utter_processing_the_request"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "Let me check",
            "Sure!",
            "I'll see what I can find out.",
            "I'll check and get back to you."
        ]
        sinhala_messages = [
            "මා එය පරීක්ෂා කර බලන්නම් ."
        ]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


class ActionUtterAskRegisteredUser(Action):  # not used in any story
    def name(self) -> Text:
        return "action_utter_ask_registered_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Are you a registered user?"]
        sinhala_messages = ["ඔබ ලියාපදිංචි පරිශීලකයෙක්ද?"]

        choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker)

        return []


def choose_and_send_message(dispatcher, english_messages, sinhala_messages, tracker):

    language = LanguageSelector.get_language(tracker)
    
    if language == SIN:
        message = random.choice(sinhala_messages)
    else:
        message = random.choice(english_messages)
    dispatcher.utter_message(text=message)
