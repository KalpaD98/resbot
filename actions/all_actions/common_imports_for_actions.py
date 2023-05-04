import logging
# noinspection PyUnresolvedReferences
from typing import Any, Dict, List, Text, Optional

# noinspection PyUnresolvedReferences
from rasa_sdk import Action, Tracker, FormValidationAction
# noinspection PyUnresolvedReferences
from rasa_sdk.events import FollowupAction, SlotSet, EventType
# noinspection PyUnresolvedReferences
from rasa_sdk.executor import CollectingDispatcher

# noinspection PyUnresolvedReferences
from submodules.database.data_models.booking import Booking
# noinspection PyUnresolvedReferences
from submodules.database.data_models.restaurant import Restaurant
# noinspection PyUnresolvedReferences
from submodules.database.data_models.user import User

# database imports
from submodules.database.repositories.booking_repository import BookingRepository
from submodules.database.repositories.restaurant_repository import RestaurantRepository
from submodules.database.repositories.user_repository import UserRepository
# noinspection PyUnresolvedReferences
from submodules.constants.constants import *
# noinspection PyUnresolvedReferences
from submodules.constants.slot_constants import *
# noinspection PyUnresolvedReferences
from submodules.constants.utterance_constants import *
# noinspection PyUnresolvedReferences
from actions.all_actions.helper_functions.response_generator.response_generator import ResponseGenerator
# noinspection PyUnresolvedReferences
from actions.all_actions.helper_functions.response_generator.constants import *
# noinspection PyUnresolvedReferences
from actions.all_actions.helper_functions.response_generator.restaurant_response_generator import RestaurantResponseGenerator
# noinspection PyUnresolvedReferences
from submodules.utils.mock_data_utils import *
# noinspection PyUnresolvedReferences
from submodules.utils.object_utils import ObjectUtils
# noinspection PyUnresolvedReferences
from submodules.utils.slot_validation_utils import SlotValidators

logger = logging.getLogger(__name__)

# initializing repositories
user_repo = UserRepository()
restaurant_repo = RestaurantRepository()
booking_repo = BookingRepository()


# print all slot values from Tracker
def print_all_slots(tracker: Tracker):  # -> List[Dict[Text, Any]]:
    print()
    print("Slots with values:")
    empty_slots = []

    for slot in tracker.slots:
        value = tracker.get_slot(slot)
        if value is not None:
            print(slot, ":", value)
        else:
            empty_slots.append(slot)

    print("\nEmpty slots: ", ", ".join(empty_slots))
    print()