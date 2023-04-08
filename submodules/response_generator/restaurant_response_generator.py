from database.models.restaurant import Restaurant
from submodules.response_generator.constants import *


class RestaurantResponseGenerator:
    @staticmethod
    def restaurant_list_to_carousal_object(restaurant_list):
        # Generate restaurant cards with Response Generator
        carousal_objects = []

        # Add data to the carousel card
        for restaurant in restaurant_list:
            carousal_object = SUBCOMPONENT_CARD.copy()
            carousal_object[TITLE] = restaurant.get(Restaurant.NAME)
            carousal_object[IMAGE_URL] = restaurant.get(Restaurant.IMAGE_URL)
            carousal_object[SUBTITLE] = restaurant.get(Restaurant.CUISINE) + " |  ⭐️ " + str(
                restaurant.get(Restaurant.RATINGS))

            default_action_payload = SUBCOMPONENT_DEFAULT_ACTION_PAYLOAD.copy()
            # determine a default action for the card later
            default_action_payload[PAYLOAD] = restaurant.get(
                Restaurant.ID)

            buttons = []

            button1 = SUBCOMPONENT_BUTTON_URL.copy()
            button1[TITLE] = "Check Menu"
            button1[URL] = restaurant.get(Restaurant.MENU_URL)  # later replace this with restaurant menu url

            button2 = SUBCOMPONENT_BUTTON_PAYLOAD.copy()
            button2[TITLE] = "Book Table"
            button2[PAYLOAD] = "/inform_booking_restaurant_id{\"restaurant_id\":\"" + restaurant.get(
                Restaurant.ID) + "\"}"
            # book table intent has not been added yet, example: book rid_s3wjdsud3, book restaurant rid_s3wjdsud3

            button3 = SUBCOMPONENT_BUTTON_PAYLOAD.copy()
            button3[TITLE] = "View Details"
            button3[PAYLOAD] = "/inform_view_details_restaurant_id{\"restaurant_id\":\"" + restaurant.get(
                Restaurant.ID) + "\"}"

            buttons.append(button1)
            buttons.append(button3)
            buttons.append(button2)

            carousal_object[BUTTONS] = buttons
            carousal_object[DEFAULT_ACTION] = ""  # set to null for temporary debugging
            # carousal_object[DEFAULT_ACTION] = default_action_payload # add a title for def action if possible
            carousal_objects.append(carousal_object)

        print(carousal_objects)
        return carousal_objects
