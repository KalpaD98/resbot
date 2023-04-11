from actions.all_actions.common_imports_for_actions import *

# CONSTANTS
ACTION_SAVE_USER_AND_COMPLETE_REGISTRATION = "action_save_user_and_complete_registration"
ACTION_RETRY_LOGIN_OR_STOP = "action_retry_login_or_stop"
ACTION_LOGIN_USER = "action_login_user"
ACTION_LOGOUT = "action_logout"
ACTION_ASK_REGISTERED_AND_SHOW_LOGIN_SIGNUP_QUICK_REPLIES = "action_ask_registered_and_show_login_signup_quick_replies"
ACTION_CHECK_USER_LOGGED_IN = "action_check_user_logged_in"
ACTION_SHOW_CUISINES = "action_show_cuisines"


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

        # if yes, utter: "User with this email already exists. Please try again with a different email."

        # if no, save user and utter: "Congratulations on completing your registration!"
        user_name = tracker.get_slot(USER_NAME)
        user_email = tracker.get_slot(USER_EMAIL)
        user_password = tracker.get_slot(USER_PASSWORD)

        # Create a UserDetails object and add it to the users list
        user = User(user_name, user_email, user_password)
        users.append(user)

        # log user in (set slots)

        # Optionally, send a confirmation message to the user
        dispatcher.utter_message(text="Congratulations on completing your registration!")

        # utter the details of the user
        dispatcher.utter_message(text="Your details are as follows:")
        dispatcher.utter_message(text="Name: " + user_name)
        dispatcher.utter_message(text="Email: " + user_email)
        # dispatcher.utter_message(text="Password: " + ObjectUtils.star_print(len(user_password)))

        return [FollowupAction(ACTION_LOGIN_USER), FollowupAction(ACTION_SHOW_CUISINES)]


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

        user = None
        # user = user = find_user_by_email(email)
        for u in users:
            if u.email == login_email:
                if u.password == login_password:
                    user = u
                    break

        if user:
            dispatcher.utter_message(template="utter_login_success")
            dispatcher.utter_message(message="Select or type a cuisine to check out restaurants.")

            return [
                SlotSet("logged_user", user),
                SlotSet("user_name", user[User.NAME]),
                SlotSet("user_id", user[User.ID]),
                SlotSet("user_email", user[User.EMAIL]),
                FollowupAction(ACTION_SHOW_CUISINES)
            ]
        else:
            dispatcher.utter_message(text="Email or password is incorrect.")
            return [
                SlotSet("logged_user", None),
                SlotSet("user_name", None),
                SlotSet("user_id", None),
                SlotSet("user_email", None),
                FollowupAction(ACTION_RETRY_LOGIN_OR_STOP)
            ]


class ActionCheckUserId(Action):

    def name(self) -> Text:
        return "action_check_user_id"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_id = tracker.get_slot("user_id")

        if user_id is None:
            # Prompt the user to log in or sign up
            dispatcher.utter_message(text="Please log in or sign up to continue.")
            # Trigger the action to show login/signup quick replies
            return [FollowupAction(ACTION_ASK_REGISTERED_AND_SHOW_LOGIN_SIGNUP_QUICK_REPLIES)]
        else:
            # Proceed with the restaurant search
            return [FollowupAction(ACTION_SHOW_CUISINES)]


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
                TITLE: "Yes",
                PAYLOAD: "/request_login_form"
            },
            {
                TITLE: "No",
                PAYLOAD: "/request_user_registration_form"
            },
            {
                TITLE: "Bye",
                PAYLOAD: "/stop"
            }
        ]

        # Generate quick replies using the ResponseGenerator class
        quick_replies = ResponseGenerator.quick_replies(quick_replies_list, with_payload=True)
        dispatcher.utter_message(text="To continue you must be logged.")
        dispatcher.utter_message(text="Are you a registered user ?", quick_replies=quick_replies)

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
            SlotSet("prevent_login_form", False)
        ]
