# from actions.all_actions.common_imports_for_actions import *
#
# ACTION_SHOW_USER_BOOKINGS = "action_show_user_bookings"
# ACTION_SHOW_PAST_BOOKINGS = "action_show_past_bookings"
# ACTION_SHOW_UPCOMING_BOOKINGS = "action_show_upcoming_bookings"
#
#
# class ActionShowUserBookings(Action):
#     def name(self) -> Text:
#         return ACTION_SHOW_USER_BOOKINGS
#
#     async def run(self, dispatcher: CollectingDispatcher,
#                   tracker: Tracker,
#                   domain: Dict[Text, Any],
#                   booking_type: str) -> List[Dict[Text, Any]]:
#
#         # can use slot user instead of user_id
#         user_id = tracker.get_slot("user_id")
#         # TODO: get user bookings from database
#         user_bookings = ["get_user_bookings(user_id, booking_type)"]
#
#         # check if bookings exist
#
#         # if no bookings exist
#         if len(user_bookings) == 0:
#             dispatcher.utter_message(text="You have no bookings")
#             return []
#
#         # Prepare carousel items / TODO: refactor this to booking response generator
#         carousel_items = []
#         for booking in user_bookings:
#             carousel_item = {
#                 "title": booking["restaurant_name"],
#                 "subtitle": f"Booking Date: {booking['booking_date']}",
#                 "image_url": booking["restaurant_image"],
#                 "buttons": [
#                     {
#                         "title": "Cancel Booking",
#                         "type": "postback",
#                         "payload": f"/inform_cancel_booking_id{{\"cancel_booking_id\": \"{booking['booking_id']}\"}}"
#                     },
#                     {
#                         "title": "Change Date",
#                         "type": "postback",
#                         "payload": f"/inform_change_date_booking_id{{\"change_booking_date_id\": \"{booking['booking_id']}\"}}"
#                     }
#                 ]
#             }
#             carousel_items.append(carousel_item)
#
#         # Send carousel to the user using your custom response generator
#         dispatcher.utter_message(
#             attachment=ResponseGenerator.card_options_carousal(carousel_items)
#         )
#
#         return []
#
#
# class ActionShowPastBookings(ActionShowUserBookings):
#     def name(self) -> Text:
#         return ACTION_SHOW_PAST_BOOKINGS
#
#     async def run(self, dispatcher: CollectingDispatcher,
#                   tracker: Tracker,
#                   domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         return await super().run(dispatcher, tracker, domain, booking_type="past")
#
#
# class ActionShowUpcomingBookings(ActionShowUserBookings):
#     def name(self) -> Text:
#         return ACTION_SHOW_UPCOMING_BOOKINGS
#
#     async def run(self, dispatcher: CollectingDispatcher,
#                   tracker: Tracker,
#                   domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         return await super().run(dispatcher, tracker, domain, booking_type="upcoming")