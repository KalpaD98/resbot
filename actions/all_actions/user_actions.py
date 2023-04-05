from actions.all_actions.common_imports import *

# CONSTANTS
ACTION_SAVE_USER_AND_COMPLETE_REGISTRATION = "action_save_user_and_complete_registration"
ACTION_RETRY_LOGIN_OR_STOP = "action_retry_login_or_stop"
ACTION_LOGIN_USER = "action_login_user"
ACTION_LOGOUT = "action_logout"


class ActionCompleteRegistration(Action):

    def name(self) -> Text:
        return "action_save_user_and_complete_registration"

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
        user_name = tracker.get_slot("user_name")
        user_email = tracker.get_slot("user_email")
        user_password = tracker.get_slot("user_password")

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
        dispatcher.utter_message(text="Password: " + ObjectUtils.star_print(len(user_password)))

        return []


class ActionLoginUser(Action):
    def name(self) -> Text:
        return "action_login_user"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        login_email = tracker.get_slot("user_email")
        login_password = tracker.get_slot("user_password")

        user = None
        # user = user = find_user_by_email(email)
        for u in users:
            if u["email"] == login_email:
                if u["password"] == login_password:
                    user = u
                    break

        if user:
            return [
                SlotSet("logged_user", user),
                SlotSet("user_name", user["name"]),
                SlotSet("user_id", user["id"]),
                SlotSet("user_email", user["email"]),
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


class ActionLogout(Action):
    def name(self) -> Text:
        return "action_logout"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [
            SlotSet("logged_user", None),
            SlotSet("user_name", None),
            SlotSet("user_id", None),
            SlotSet("user_email", None),
            SlotSet("password", None),
        ]
