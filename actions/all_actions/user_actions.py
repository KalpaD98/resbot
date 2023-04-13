from actions.all_actions.common_imports_for_actions import *

# CONSTANTS
ACTION_SAVE_USER_AND_COMPLETE_REGISTRATION = "action_save_user_and_complete_registration"
ACTION_RETRY_LOGIN_OR_STOP = "action_retry_login_or_stop"
ACTION_LOGIN_USER = "action_login_user"
ACTION_LOGOUT = "action_logout"
ACTION_ASK_REGISTERED_AND_SHOW_LOGIN_SIGNUP_QUICK_REPLIES = "action_ask_registered_and_show_login_signup_quick_replies"
ACTION_CHECK_USER_ID = "action_check_user_id"
ACTION_SHOW_CUISINES = "action_show_cuisines"
ACTION_ASK_WHAT_USER_WANTS = "action_ask_what_user_wants"


class ActionCompleteRegistration(Action):

    def name(self) -> Text:
        return ACTION_SAVE_USER_AND_COMPLETE_REGISTRATION

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # check of user with mail already exists

        # set slots to None

        # Create a User and save them in the database
        user_name = tracker.get_slot(USER_NAME)
        user_email = tracker.get_slot(USER_EMAIL)
        user_password = tracker.get_slot(USER_PASSWORD)

        user = User(user_name, user_email, user_password)

        user_id = user_repo.insert_user(user)

        if user_id is None:
            dispatcher.utter_message(
                text="Registration failed. Please try again.")
            return [FollowupAction(ACTION_ASK_REGISTERED_AND_SHOW_LOGIN_SIGNUP_QUICK_REPLIES)]

        # Set user details in the tracker

        # Send a confirmation message to the user
        dispatcher.utter_message(text="Congratulations on completing your registration " + user.name + "!")

        # utter the details of the user
        dispatcher.utter_message(text="Your details are as follows:")
        dispatcher.utter_message(text="Name: " + user.name)
        dispatcher.utter_message(text="Email: " + user.email)
        dispatcher.utter_message(text="You have been automatically logged in.")
        # TODO: quick reply to continue conversation
        # dispatcher.utter_message(text="Password: " + ObjectUtils.star_print(len(user_password)))

        return [
            SlotSet(LOGGED_USER, user),
            SlotSet(USER_ID, user_id),
            SlotSet(USER_NAME, user.name),
            SlotSet(USER_EMAIL, user.email),
            SlotSet(USER_PASSWORD, user.password),
            SlotSet(IS_AUTHENTICATED, True)
        ]


class ActionLoginUser(Action):
    def name(self) -> Text:
        return ACTION_LOGIN_USER

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        login_email = tracker.get_slot(USER_EMAIL)
        login_password = tracker.get_slot(USER_PASSWORD)

        user = user_repo.find_user_by_email(login_email)

        if user is None:
            dispatcher.utter_message(
                text="User with the email provided does not exist. Please try again with a different email.")
            return [
                SlotSet(LOGGED_USER, None),
                SlotSet(USER_NAME, None),
                SlotSet(USER_ID, None),
                SlotSet(USER_EMAIL, None),
                SlotSet(USER_PASSWORD, None),
                SlotSet(IS_AUTHENTICATED, False),
                FollowupAction(ACTION_RETRY_LOGIN_OR_STOP)
            ]
        # authenticate the user
        if user.password == login_password:

            quick_replies_with_payload = []

            quick_reply_request_restaurant = {
                TITLE: "Checkout restaurants",
                PAYLOAD: "/request_restaurants"}

            quick_reply_search_restaurants = {
                TITLE: "Search restaurants",
                PAYLOAD: "/search_restaurants"}

            quick_replies_with_payload.append(quick_reply_request_restaurant)
            quick_replies_with_payload.append(quick_reply_search_restaurants)

            dispatcher.utter_message(response="utter_login_success",
                                     quick_replies=ResponseGenerator.quick_replies(quick_replies_with_payload, True))

            return [
                SlotSet(LOGGED_USER, user.to_dict()),
                SlotSet(USER_NAME, user.name),
                SlotSet(USER_ID, user.id),
                SlotSet(USER_EMAIL, user.email),
                SlotSet(USER_PASSWORD, user.password),
                SlotSet(IS_AUTHENTICATED, True),
            ]

        else:
            dispatcher.utter_message(text="password is incorrect.")
            return [
                SlotSet(LOGGED_USER, None),
                SlotSet(USER_NAME, None),
                SlotSet(USER_ID, None),
                SlotSet(USER_EMAIL, None),
                FollowupAction(ACTION_RETRY_LOGIN_OR_STOP)
            ]


class ActionRetryLoginOrStop(Action):
    def name(self) -> Text:
        return ACTION_RETRY_LOGIN_OR_STOP

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        quick_replies_with_payload = []

        quick_reply_retry = {
            TITLE: "Yes",
            PAYLOAD: "/request_login_form"}

        quick_reply_stop = {
            TITLE: "No",
            PAYLOAD: "/stop"}

        quick_replies_with_payload.append(quick_reply_retry)
        quick_replies_with_payload.append(quick_reply_stop)

        dispatcher.utter_message(text="Would you like to retry logging in?",
                                 quick_replies=ResponseGenerator.quick_replies(quick_replies_with_payload, True))

        return []


class ActionAskRegisteredAndShowLoginSignupQuickReplies(Action):
    def name(self) -> Text:
        return ACTION_ASK_REGISTERED_AND_SHOW_LOGIN_SIGNUP_QUICK_REPLIES

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Define quick replies
        quick_replies_list = [
            {
                TITLE: "Login",
                PAYLOAD: "/request_login_form"
            },
            {
                TITLE: "Register",
                PAYLOAD: "/request_user_registration_form"
            }
        ]

        # Generate quick replies using the ResponseGenerator class
        quick_replies = ResponseGenerator.quick_replies(quick_replies_list, with_payload=True)
        dispatcher.utter_message(text="Please log in or sign up to continue.", quick_replies=quick_replies)

        return []


class ActionLogout(Action):
    def name(self) -> Text:
        return ACTION_LOGOUT

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [
            SlotSet("logged_user", None),
            SlotSet("user_name", None),
            SlotSet("user_id", None),
            SlotSet("user_email", None),
            SlotSet("password", None),
            SlotSet(IS_AUTHENTICATED, False),
        ]
