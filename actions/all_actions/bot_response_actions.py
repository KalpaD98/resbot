import random

from actions.all_actions.common_imports_for_actions import *


class UtterGreet(Action):
    def name(self) -> Text:
        return "action_utter_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Hi!", "Hey!", "Hello!", "Hi 😃 there!", "Hello there 😀"]
        choose_and_send_message(english_messages)

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
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterGreetAgain(Action):
    def name(self) -> Text:
        return "action_utter_greet_again"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Hi there again!", "Hello again!"]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterMoodGreatFeedback(Action):
    def name(self) -> Text:
        return "action_utter_mood_great_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Cool! 😎", "Nice to hear 😃 that", "Happy to hear 😊"]
        choose_and_send_message(dispatcher, english_messages)

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
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterEmojiGreatFeedback(Action):
    def name(self) -> Text:
        return "action_utter_emoji_great_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["😊", "😄"]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterEmojiMoodUnhappyFeedback(Action):
    def name(self) -> Text:
        return "action_utter_emoji_mood_unhappy_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Eating something might help 🤗", "Eating something might help 😊"]
        choose_and_send_message(dispatcher, english_messages)

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
        choose_and_send_message(dispatcher, english_messages)

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
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterGoodbye(Action):
    def name(self) -> Text:
        return "action_utter_goodbye"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Bye", "Goodbye", "Farewell", "See you later"]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterBotIntro(Action):
    def name(self) -> Text:
        return "action_utter_bot_intro"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "I'm ResBot! 🍴, I can recommend amazing restaurants and make reservations seamless for you 🌟.",
            "I'm ResBot, your dining assistant. I help find ideal restaurants and make reservations for you 🌟."
        ]
        choose_and_send_message(dispatcher, english_messages)

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
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterByeSeeYouLater(Action):
    def name(self) -> Text:
        return "action_utter_bye_see_you_later"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Good Bye. See you later!"]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterProcessingTheRequest(Action):
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
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterAskRegisteredUser(Action):
    def name(self) -> Text:
        return "action_utter_ask_registered_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Are you a registered user?"]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterAskUserName(Action):
    def name(self) -> Text:
        return "action_utter_ask_user_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "May I know your name? (first name is sufficient)"
        ]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterAskUserEmail(Action):
    def name(self) -> Text:
        return "action_utter_ask_user_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Enter your email address."]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterAskUserPassword(Action):
    def name(self) -> Text:
        return "action_utter_ask_user_password"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Enter password."]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterRegistrationSuccessful(Action):
    def name(self) -> Text:
        return "action_utter_registration_successful"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot("user_name")
        english_messages = [
            f"Registration successful! We automatically logged you {user_name}"
        ]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterLoginSuccess(Action):
    def name(self) -> Text:
        return "action_utter_login_success"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["You have successfully logged in. Welcome back!"]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterLoginToContinue(Action):
    def name(self) -> Text:
        return "action_utter_login_to_continue"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Please login to continue."]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterAlreadyLoggedIn(Action):
    def name(self) -> Text:
        return "action_utter_already_logged_in"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["You are already logged in."]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterAskDate(Action):
    def name(self) -> Text:
        return "action_utter_ask_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "When would you like to make the booking? A future date (tomorrow or later) "
            "in the format [YYYY/MM/DD] is preferred",
            "What date do you have in mind for the booking?  A future date (tomorrow or later) "
            "in the format [YYYY/MM/DD] is preferred"
        ]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterAskNumPeople(Action):
    def name(self) -> Text:
        return "action_utter_ask_num_people"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "May I know the number of people for the booking?",
            "For how many people are you planing to make the reservation?"
        ]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterAskCancelBookingConfirmation(Action):
    def name(self) -> Text:
        return "action_utter_ask_cancel_booking_confirmation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        restaurant = tracker.get_slot("restaurant")
        selected_booking = tracker.get_slot("selected_booking")
        num_people = tracker.get_slot("num_people")
        english_messages = [
            f"Are you sure you want to cancel the booking at {restaurant['name']} on {selected_booking['date']} "
            f"for {num_people} people? This action cannot be undone."
        ]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterAskCancelAnotherBooking(Action):
    def name(self) -> Text:
        return "action_utter_ask_cancel_another_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Do you want to cancel another booking?"]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterAskNewBookingDate(Action):
    def name(self) -> Text:
        return "action_utter_ask_new_booking_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["What is the new date for the booking?"]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterAskChangeAnotherBooking(Action):
    def name(self) -> Text:
        return "action_utter_ask_change_another_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Do you want to change another booking?"]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterNoBookingsFound(Action):
    def name(self) -> Text:
        return "action_utter_no_bookings_found"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Sorry, there are no bookings found for you."]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterAskTryAgain(Action):
    def name(self) -> Text:
        return "action_utter_ask_try_again"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "Would you like to try again?",
            "Do you want to try searching again?"
        ]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterAskDifferentDate(Action):
    def name(self) -> Text:
        return "action_utter_ask_different_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "Would you like to select a different date for the booking?",
            "Do you want to choose another date for the reservation?"
        ]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterAskDifferentRestaurant(Action):
    def name(self) -> Text:
        return "action_utter_ask_different_restaurant"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = [
            "Would you like to choose a different restaurant?",
            "Do you want to look for another restaurant?"
        ]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterBookingConfirmation(Action):
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
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterNoPastBookingsFound(Action):
    def name(self) -> Text:
        return "action_utter_no_past_bookings_found"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Sorry, there are no past bookings found for you."]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterNoFutureBookingsFound(Action):
    def name(self) -> Text:
        return "action_utter_no_future_bookings_found"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["Sorry, there are no upcoming bookings found for you."]
        choose_and_send_message(dispatcher, english_messages)

        return []


class ActionUtterNoChangesMadeToBooking(Action):
    def name(self) -> Text:
        return "action_utter_no_changes_made_to_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        english_messages = ["No changes were made to your booking"]
        choose_and_send_message(dispatcher, english_messages)

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
        choose_and_send_message(dispatcher, english_messages)

        return []


def choose_and_send_message(dispatcher, messages):
    message = random.choice(messages)
    dispatcher.utter_message(text=message)
