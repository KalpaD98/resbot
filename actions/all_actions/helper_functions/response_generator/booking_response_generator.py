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

            carousel_object[TITLE] = "🍽️ at " + restaurant.name + "for " + number_to_word(booking.num_people)
            carousel_object[IMAGE_URL] = restaurant.image_url
            carousel_object[SUBTITLE] = f"📅: {booking.date}"

            booking_date = datetime.strptime(booking.date, "%Y-%m-%d").date()
            current_date = datetime.now().date()

            buttons = []

            if booking_date > current_date:
                button1 = SUBCOMPONENT_BUTTON_PAYLOAD.copy()
                button1[TITLE] = "Cancel Booking"
                button1[PAYLOAD] = f"/inform_cancel_booking_id{{\"booking_id\": \"{booking.id}\"}}"
                buttons.append(button1)

                button2 = SUBCOMPONENT_BUTTON_PAYLOAD.copy()
                button2[TITLE] = "Change Booking"
                button2[PAYLOAD] = f"/inform_change_booking_id{{\"booking_id\": \"{booking.id}\"}}"
                buttons.append(button2)

            carousel_object[BUTTONS] = buttons
            carousel_object[DEFAULT_ACTION] = ""

            # add the carousel object to the list
            carousel_objects.append(carousel_object)

        return carousel_objects

    @staticmethod
    def generate_booking_details_text(booking, restaurant):
        booking_details = (
            f"Booking Details:\n\n"
            f"Restaurant: {restaurant.name}\n"
            f"Address: {restaurant.address}\n"
            f"Date: {booking.date}\n"
            f"Time: {booking.time if booking.time else 'Not specified'}\n"
            f"Number of people: {booking.num_people}\n"
        )
        return booking_details

    @staticmethod
    def generate_booking_comparison_text(old_booking, new_booking, restaurant):

        comparison_text = "Here is a comparison of your booking details:\n\n"
        comparison_text += f"Restaurant: {restaurant.name}\n"
        comparison_text += f"Address: {restaurant.address}\n"
        # f"Time: {old_booking.time if old_booking.time else 'Not specified'}\n"

        if old_booking.date != new_booking.date:
            comparison_text += f"Date: {old_booking.date} -> {new_booking.date}\n"

        if old_booking.num_people != new_booking.num_people:
            comparison_text += f"Number of people: {old_booking.num_people} -> {new_booking.num_people}\n"

        return comparison_text


def number_to_word(n: int) -> str:
    num_to_word = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten",
    }

    return num_to_word.get(n, "")
