import sys

from actions.submodules.constants import *

sys.path.append("/actions/submodules")


class RestaurantUtils:
    @staticmethod
    def restaurant_list_to_carousal_object(restaurant_list):
        # Generate restaurant cards with Response Generator
        carousal_objects = []

        # Add data to the carousel card
        for restaurant in restaurant_list:
            carousal_object = SUBCOMPONENT_CARD.copy()
            carousal_object[TITLE] = restaurant.get(NAME)
            carousal_object[IMAGE_URL] = restaurant.get(IMAGE_URL)
            carousal_object[SUBTITLE] = restaurant.get(CUISINE) + " |  ⭐️ " + str(restaurant.get(RATINGS))

            default_action_payload = SUBCOMPONENT_DEFAULT_ACTION_PAYLOAD.copy()
            default_action_payload[PAYLOAD] = restaurant.get(ID)  # determine a default action for the card later

            buttons = []

            button1 = SUBCOMPONENT_BUTTON_URL.copy()
            button1[TITLE] = "Check Menu"
            button1[URL] = restaurant.get(MENU_URL)  # later replace this with restaurant menu url

            button2 = SUBCOMPONENT_BUTTON_PAYLOAD.copy()
            button2[TITLE] = "Book Table"
            button2[PAYLOAD] = "/inform_booking_restaurant_id{\"restaurant_id\":\"" + restaurant.get(ID) + "\"}"
            # book table intent has not been added yet, example: book rtid_s3wjdsud3, book restaurant rtid_s3wjdsud3

            button3 = SUBCOMPONENT_BUTTON_PAYLOAD.copy()
            button3[TITLE] = "View Details"
            button3[PAYLOAD] = "/inform_view_details_restaurant_id{\"restaurant_id\":\"" + restaurant.get(ID) + "\"}"

            buttons.append(button1)
            buttons.append(button3)
            buttons.append(button2)

            carousal_object[BUTTONS] = buttons
            carousal_object[DEFAULT_ACTION] = ""  # set to null for temporary debugging
            # carousal_object[DEFAULT_ACTION] = default_action_payload # add a title for def action if possible
            carousal_objects.append(carousal_object)

        print(carousal_objects)
        return carousal_objects
