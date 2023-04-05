from actions.all_actions.common_imports import *

# constants
ACTION_SHOW_SELECTED_RESTAURANT_DETAILS = "action_show_selected_restaurant_details"
ACTION_SHOW_SELECTED_RESTAURANT_ASK_BOOKING_CONFIRMATION = "action_show_selected_restaurant_ask_booking_confirmation"
ACTION_SHOW_BOOKING_SUMMARY = "action_show_booking_summary"
ACTION_CONFIRM_BOOKING = "action_confirm_booking"


# action_show_selected_restaurant_ask_booking_confirmation.
class ActionBookSelectedRestaurant(Action):
    def name(self) -> Text:
        return ACTION_SHOW_SELECTED_RESTAURANT_ASK_BOOKING_CONFIRMATION

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print_slots(tracker)

        # get the restaurant id from the tracker
        restaurant_id = tracker.get_slot("restaurant_id")

        if restaurant_id is None:
            logging.info("Restaurant ID not set")
            dispatcher.utter_message(text="Cannot show restaurant details. Please select a restaurant first.")
            return []

        # get the restaurant details by passing the id
        restaurant = ObjectUtils.find_by_id(restaurant_id, rest_list)
        # logging.info(restaurant)

        y_n_quick_replies_with_payload = []

        quick_reply_yes = {
            TITLE: QR_YES,
            PAYLOAD: "/affirm"}

        quick_reply_no = {
            TITLE: QR_NO,
            PAYLOAD: "/deny"}

        y_n_quick_replies_with_payload.append(quick_reply_yes)
        y_n_quick_replies_with_payload.append(quick_reply_no)
        # send the message back to the user
        dispatcher.utter_message(text="You selected " + restaurant[NAME])
        # add multiple messages for each below
        # dispatcher.utter_message(text="<small description>, <address>, <Opening hours [weekend,weekdays]>")
        dispatcher.utter_message(text="Would you like to proceed with the booking?",
                                 quick_replies=ResponseGenerator.quick_replies(y_n_quick_replies_with_payload, True))
        # if yes -> fill slot
        return [SlotSet(SELECTED_RESTAURANT, restaurant)]
        # if no
        # Clear the slots related to restaurant selection


# action_show_selected_restaurant_details.
# This function will fetch data of the selected restaurant and send it in the message.
# This will include a small description about the restaurant, its address and opening hours.
class ActionShowSelectedRestaurantDetails(Action):
    def name(self) -> Text:
        return ACTION_SHOW_SELECTED_RESTAURANT_DETAILS

    # async run function to fetch restaurant data from the db_knowledge base

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print_slots(tracker)

        # get the restaurant id from the tracker
        restaurant_id = tracker.get_slot("restaurant_id")

        if restaurant_id is None:
            dispatcher.utter_message(text="Cannot show restaurant details. Please select a restaurant first.")
            return []

        # restaurant = await self.db_knowledge.get_object("restaurant", restaurant_id)

        # Send the image to the user
        # dispatcher.utter_message(image=image_path)

        # get the restaurant details by passing the id
        restaurant = ObjectUtils.find_by_id(restaurant_id, rest_list)
        logging.info(restaurant)

        # send the message back to the user

        dispatcher.utter_message(image=restaurant[IMAGE_URL])
        dispatcher.utter_message(
            text=restaurant[NAME] + " mainly serves " + restaurant[CUISINE] + " food and its located at "
                                                                              "" + restaurant[ADDRESS])
        dispatcher.utter_message(text="Their opening hours are, ")
        dispatcher.utter_message(text="Mon - Fri: " + restaurant[OPENING_HOURS][MON_TO_FRI])
        dispatcher.utter_message(text="Sat - Sun: " + restaurant[OPENING_HOURS][SAT_SUN])

        dispatcher.utter_message(
            text=ObjectUtils.get_random_sentence(restaurant[NAME], UTTER_SENTENCE_LIST_FOR_ASKING_TO_MAKE_RESERVATION),
            quick_replies=ResponseGenerator.quick_replies([QR_YES, QR_NO]))

        return [SlotSet("selected_restaurant", restaurant), SlotSet("restaurant_id", restaurant_id)]


# action_show_booking_summary.
# This function is used to generate a booking summary and send it to the user as a message.
class ActionShowBookingSummary(Action):

    # action name
    def name(self) -> Text:
        return ACTION_SHOW_BOOKING_SUMMARY

    # async run function to generate booking summary that include restaurant, restaurant address, date and time.

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print_slots(tracker)

        # get restaurant id from the tracker
        # restaurant_id = tracker.get_slot("restaurant_id")

        # get the restaurant data from the db_knowledge base
        # restaurant = await self.db_knowledge.get_object("restaurant", restaurant_id)

        # get the date from the tracker
        date = tracker.get_slot("date")
        time = tracker.get_slot("time")
        restaurant = tracker.get_slot(SELECTED_RESTAURANT)
        # send the message to the user
        dispatcher.utter_message(
            text="Your booking summary for " + restaurant[NAME] + " is as follows:")
        # generate the booking summary
        dispatcher.utter_message(text="Number of people: " + tracker.get_slot(NUM_PEOPLE))
        dispatcher.utter_message(text="Date: " + date)
        if time is not None:
            dispatcher.utter_message(text="Time: " + time)

        # ask to confirm the booking

        # TODO: if no -> ask if they would like to book a table of another restaurant or exit

        dispatcher.utter_message(text="Would you like to confirm this booking?",
                                 quick_replies=ResponseGenerator.quick_replies([QR_YES, QR_NO]))
        # "Please choose a cuisine",
        # if yes
        return []
        # if no clear restaurant  slots by far


# action_confirm_booking.
# This function is used to confirm the booking and send a message to the user based on their response.
# run this function after confirming the booking.
class ActionConfirmBooking(Action):
    def name(self) -> Text:
        return ACTION_CONFIRM_BOOKING

    # run method to confirm the booking, save on database and send a message to the user based on their response

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print_slots(tracker)

        # get the restaurant id from the tracker
        restaurant_id = tracker.get_slot("restaurant_id")
        user_id = tracker.get_slot("user_id")

        # get the restaurant data from the db_knowledge base
        # restaurant = self.db_knowledge.get_object("restaurant", restaurant_id)

        # get the date from the tracker
        date = tracker.get_slot("date")
        if date is None:
            logging.info("Date not set")

        selected_restaurant = tracker.get_slot(SELECTED_RESTAURANT)

        # generate the booking summary
        message = "Your booking for " + selected_restaurant[NAME] + " located at " + selected_restaurant[ADDRESS] + \
                  " on " + date + " has been confirmed"

        # send the message to the user
        dispatcher.utter_message(text=message)
        dispatcher.utter_message(text="Your booking reference id is: brid_1FK2H1G3")

        return []


class ActionShowUserBookings(Action):
    def name(self) -> Text:
        return "action_show_user_bookings"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any],
                  booking_type: str) -> List[Dict[Text, Any]]:
        user_id = tracker.get_slot("user_id")
        user_bookings = get_user_bookings(user_id, booking_type)

        # Prepare carousel items
        carousel_items = []
        for booking in user_bookings:
            carousel_item = {
                "title": booking["restaurant_name"],
                "subtitle": f"Booking Date: {booking['booking_date']}",
                "image_url": booking["restaurant_image"],
                "buttons": [
                    {
                        "title": "Cancel Booking",
                        "type": "postback",
                        "payload": f"/inform_cancel_booking_id{{\"cancel_booking_id\": \"{booking['booking_id']}\"}}"
                    },
                    {
                        "title": "Change Date",
                        "type": "postback",
                        "payload": f"/inform_change_date_booking_id{{\"change_booking_date_id\": \"{booking['booking_id']}\"}}"
                    }
                ]
            }
            carousel_items.append(carousel_item)

        # Send carousel to the user using your custom response generator
        dispatcher.utter_message(
            attachment=ResponseGenerator.card_options_carousal(carousel_items)
        )

        return []


class ActionShowPastBookings(ActionShowUserBookings):
    def name(self) -> Text:
        return "action_show_past_bookings"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return await super().run(dispatcher, tracker, domain, booking_type="past")


class ActionShowUpcomingBookings(ActionShowUserBookings):
    def name(self) -> Text:
        return "action_show_upcoming_bookings"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return await super().run(dispatcher, tracker, domain, booking_type="upcoming")


class ActionChangeBookingDate(Action):
    def name(self) -> Text:
        return "action_change_restaurant_booking_date"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        booking_id = tracker.get_slot("booking_id")
        new_date = tracker.get_slot("date")

        # Update the booking date in system here.
        # call  API to update database.

        # Send a confirmation message to the user
        dispatcher.utter_message(text=f"Your booking with ID {booking_id} has been successfully updated to {new_date}.")
        return [SlotSet("date", None)]


class ActionShowNewBookingDetails(Action):

    def name(self) -> Text:
        return "action_show_new_booking_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        booking_id = tracker.get_slot("booking_id")
        date = tracker.get_slot("date")

        # Mock booking details
        booking_details = {
            'booking_id': 'bid_123',
            'restaurant_name': 'The Fancy Restaurant',
            'date': '2023-03-30',
            # 'time': '19:00',
            'num_people': 4
        }

        if booking_details is not None:
            # Update the booking date in the booking_details
            booking_details['date'] = date

            # Format the message to show the updated booking details
            message = f"Here are the updated booking details:\n\n"
            message += f"Booking ID: {booking_details['booking_id']}\n"
            message += f"Restaurant: {booking_details['restaurant_name']}\n"
            message += f"Date: {booking_details['date']}\n"
            # message += f"Time: {booking_details['time']}\n"
            message += f"Number of people: {booking_details['num_people']}\n"

            dispatcher.utter_message(text=message)
            dispatcher.utter_message(text="would you like to confirm the change?")
            dispatcher.utter_message(quickreplies=ResponseGenerator.quick_replies([QR_YES, QR_NO]))
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find the booking details.")

        return []


class ActionCancelBooking(Action):
    def name(self) -> Text:
        return "action_cancel_booking"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[EventType]:
        cancel_booking_id = tracker.get_slot("cancel_booking_id")

        # Fetch booking information from the database using cancel_booking_id (customize this part)
        booking = {
            "booking_id": "bid_123",
            "restaurant_name": "Restaurant A",
            "booking_date": "2023-06-10",
            "num_people": 4
        }

        # Cancel the booking in the database using cancel_booking_id (customize this part)
        # Add a comment to indicate where the database operation should be done
        # For example: Cancel booking in the database using cancel_booking_id

        message = f"Your booking at {booking['restaurant_name']} on {booking['booking_date']} for {booking['num_people']} people has been successfully canceled."

        # Clear the cancel_booking_id slot
        return [SlotSet("cancel_booking_id", None), dispatcher.utter_message(text=message)]


class ActionAskCancelBookingConfirmation(Action):
    def name(self) -> Text:
        return "action_ask_cancel_booking_confirmation"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cancel_booking_id = tracker.get_slot("cancel_booking_id")

        # Fetch booking information from the database using cancel_booking_id (customize this part)
        booking = {
            "booking_id": "bid_123",
            "restaurant_name": "Restaurant A",
            "booking_date": "2023-06-10",
            "num_people": 4
        }

        # change formatting of below message
        message = f"Are you sure you want to cancel the booking for {booking['restaurant_name']} on {booking['booking_date']} for {booking['num_people']} people? This action cannot be undone."

        dispatcher.utter_message(text=message)

        return []
