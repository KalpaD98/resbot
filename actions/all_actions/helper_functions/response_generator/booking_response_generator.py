from datetime import datetime

# booking_response_generator.py
from actions.all_actions.helper_functions.response_generator.constants import *


class BookingResponseGenerator:
    @staticmethod
    def booking_list_to_carousal_object(booking_list, restaurant_data_dict):
        carousel_objects = []

        for booking in booking_list:
            carousel_object = SUBCOMPONENT_CARD.copy()

            restaurant = restaurant_data_dict[booking.restaurant_id]

            carousel_object[TITLE] = restaurant.name
            carousel_object[IMAGE_URL] = restaurant.image_url
            carousel_object[SUBTITLE] = f"Booking Date: {booking.date}"

            booking_date = datetime.strptime(booking.date, "%Y-%m-%d").date()
            current_date = datetime.now().date()

            buttons = []

            if booking_date > current_date:
                button1 = SUBCOMPONENT_BUTTON_PAYLOAD.copy()
                button1[TITLE] = "Cancel Booking"
                button1[PAYLOAD] = f"/inform_cancel_booking_id{{\"booking_id\": \"{booking.id}\"}}"
                buttons.append(button1)

                button2 = SUBCOMPONENT_BUTTON_PAYLOAD.copy()
                button2[TITLE] = "Change Date"
                button2[
                    PAYLOAD] = f"/inform_change_date_booking_id{{\"booking_id\": \"{booking.id}\"}}"
                buttons.append(button2)

            carousel_object[BUTTONS] = buttons
            carousel_object[DEFAULT_ACTION] = ""

            # add the carousel object to the list
            carousel_objects.append(carousel_object)

        return carousel_objects
