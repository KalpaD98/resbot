import logging

from actions.all_actions.common_imports_for_actions import restaurant_repo
from submodules.constants.slot_constants import RESTAURANT_ID


def get_restaurant(tracker, dispatcher):
    # Get the restaurant ID from the tracker
    restaurant_id = tracker.get_slot(RESTAURANT_ID)

    if restaurant_id is None:
        logging.error("Restaurant ID not set")
        dispatcher.utter_message(text="An error occurred while selecting the restaurant.")
        return None

    # Get the restaurant details by passing the ID
    restaurant = restaurant_repo.find_restaurant_by_id(restaurant_id=restaurant_id)

    if restaurant is None:
        logging.error("Restaurant not found")
        dispatcher.utter_message(text="An error occurred while fetching the restaurant.")
        return None

    return restaurant
