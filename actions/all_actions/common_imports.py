import logging
from typing import Any, Dict, List, Text, Optional

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import FollowupAction, SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher

from actions.submodules.constants.constants import *

from actions.submodules.entities.user import User

from actions.submodules.persistance.bookings import get_user_bookings

from actions.submodules.utils.mock_data_utils import *
from actions.submodules.utils.object_utils import ObjectUtils
from actions.submodules.utils.slot_validation_utils import SlotValidators
from actions.submodules.utils.response_generation_utils import ResponseGenerator
from actions.submodules.utils.restaurant_response_generation_utils import RestaurantResponseGenerationUtils

logger = logging.getLogger(__name__)


# print all slot values from Tracker
def print_slots(tracker: Tracker):  # -> List[Dict[Text, Any]]:
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

######################################################## Backup ########################################################

# import logging
# from typing import Any, Dict, List, Text, Optional
#
# from rasa_sdk import Action, Tracker, FormValidationAction
# from rasa_sdk.events import FollowupAction, SlotSet, EventType
# from rasa_sdk.executor import CollectingDispatcher
#
# from actions.submodules.constants.constants import *
#
# from actions.submodules.entities.user import User
#
# from actions.submodules.persistance.bookings import get_user_bookings
#
# from actions.submodules.utils.mock_data_utils import *
# from actions.submodules.utils.object_utils import ObjectUtils
# from actions.submodules.utils.slot_validation_utils import SlotValidators
# from actions.submodules.utils.response_generation_utils import ResponseGenerator
# from actions.submodules.utils.restaurant_response_generation_utils import RestaurantResponseGenerationUtils
