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
                button2[PAYLOAD] = f"/inform_change_date_booking_id{{\"booking_id\": \"{booking.id}\"}}"
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

        if booking.special_requests:
            booking_details += f"Special requests: {booking.special_requests}\n"

        return booking_details

    @staticmethod
    def generate_booking_comparison_text(old_booking, new_booking, restaurant):
        comparison_text = "Here is a comparison of your booking details:\n\n"

        if old_booking.date != new_booking.date:
            comparison_text += f"Date: {old_booking.date} -> {new_booking.date}\n"

        if old_booking.num_people != new_booking.num_people:
            comparison_text += f"Number of people: {old_booking.num_people} -> {new_booking.num_people}\n"

        comparison_text += (
            f"\nRestaurant: {restaurant.name}\n"
            f"Address: {restaurant.address}\n"
            f"Time: {old_booking.time if old_booking.time else 'Not specified'}\n"
        )

        if old_booking.special_requests:
            comparison_text += f"Special requests: {old_booking.special_requests}\n"

        comparison_text += "\nDo you want to confirm these changes?"
        return comparison_text
