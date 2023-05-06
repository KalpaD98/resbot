from datetime import datetime

# booking_response_generator.py
from actions.all_actions.helper_functions.response_generator.constants import *


class BookingResponseGenerator:
    @staticmethod
    def booking_list_to_carousal_object(booking_list, restaurant_data_dict, language=EN):
        carousel_objects = []

        for booking in booking_list:
            carousel_object = SUBCOMPONENT_CARD.copy()

            restaurant = restaurant_data_dict[booking.restaurant_id]

            carousel_object[TITLE] = "🍽️ at " + restaurant.name + " for " + str(booking.num_people)

            if language == SIN:
                carousel_object[TITLE] = "🍽️ " + restaurant.name + " හි සහභාගිවන්නන්" + str(booking.num_people) + "ක් සදහා"

            carousel_object[IMAGE_URL] = restaurant.image_url
            booking_date = datetime.strptime(booking.date, "%Y-%m-%d").date()
            formatted_date = booking_date.strftime("%Y/%m/%d")
            carousel_object[SUBTITLE] = f"📅: {formatted_date}"

            current_date = datetime.now().date()

            buttons = []

            if booking_date > current_date:
                button1 = SUBCOMPONENT_BUTTON_PAYLOAD.copy()
                button1[TITLE] = ("Booking එක අවලංගු කරන්න" if language == SIN else "Cancel Booking")
                button1[PAYLOAD] = f"/inform_cancel_booking_id{{\"booking_id\": \"{booking.id}\"}}"
                buttons.append(button1)

                button2 = SUBCOMPONENT_BUTTON_PAYLOAD.copy()
                button2[TITLE] = ("Booking එක වෙනස් කරන්න" if language == SIN else "Change Booking")
                button2[PAYLOAD] = f"/inform_change_booking_id{{\"booking_id\": \"{booking.id}\"}}"
                buttons.append(button2)

            carousel_object[BUTTONS] = buttons
            carousel_object[DEFAULT_ACTION] = ""

            # add the carousel object to the list
            carousel_objects.append(carousel_object)

        return carousel_objects

    @staticmethod
    def generate_booking_details_text(booking, restaurant, language=EN):
        booking_details = (
            f"Booking Details:\n\n"
            f"Restaurant: {restaurant.name}\n"
            f"Address: {restaurant.address}\n"
            f"Date: {booking.date}\n"
            f"Time: {booking.time if booking.time else 'Not specified'}\n"
            f"Number of people: {booking.num_people}\n"
        )

        if language == SIN:
            booking_details = (
                f"Booking විස්තර:\n\n"
                f"ආපන ශාලාව: {restaurant.name}\n"
                f"ලිපිනය: {restaurant.address}\n"
                f"දිනය: {booking.date}\n"
                f"වේලාව: {booking.time if booking.time else 'Not specified'}\n"
                f"පුද්ගලයන් ගනන: {booking.num_people}\n"
            )

        return booking_details

    @staticmethod
    def generate_booking_comparison_text(old_booking, new_booking, restaurant, language=EN):

        comparison_text = "Here is a comparison of your booking details:\n\n"
        comparison_text += f"Restaurant: {restaurant.name}\n\n"
        comparison_text += f"Address: {restaurant.address}\n\n"
        # f"Time: {old_booking.time if old_booking.time else 'Not specified'}\n"

        if old_booking.date != new_booking.date:
            comparison_text += f"Date: {old_booking.date} -> {new_booking.date}\n\n"

        if old_booking.num_people != new_booking.num_people:
            comparison_text += f"Number of people: {old_booking.num_people} -> {new_booking.num_people}\n"

        if language == SIN:
            comparison_text = "ඔබේ වෙන්කිරීමේ විස්තර සංසන්දනය කිරීම:\n\n"
            comparison_text += f"ආපන ශාලාව: {restaurant.name}\n\n"
            comparison_text += f"ලිපිනය: {restaurant.address}\n\n"
            # f"Time: {old_booking.time if old_booking.time else 'Not specified'}\n"

            if old_booking.date != new_booking.date:
                comparison_text += f"දිනය: {old_booking.date} -> {new_booking.date}\n\n"

            if old_booking.num_people != new_booking.num_people:
                comparison_text += f"පුද්ගලයන් ගනන: {old_booking.num_people} -> {new_booking.num_people}\n"

        return comparison_text
