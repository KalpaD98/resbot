# constant.py contains all the constants used in the project

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ------------------------------------------ Response Generator Constants ------------------------------------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

TYPE = "type"
TEMPLATE = "template"
PAYLOAD = "payload"
TEMPLATE_TYPE = "template_type"
GENERIC = "generic"
ELEMENTS = "elements"
DEFAULT_ACTION = "default_action"
WEB_URL = "web_url"
POST_BACK = "postback"
URL = "url"
TITLE = "title"
SUBTITLE = "subtitle"
BUTTONS = "buttons"
HOME_PAGE = "home_page"

# --- ----- ----- ----- ----- ----- -----  ----- ----- Components ----- ----- ----- ----- ----- ----- ----- -----  --- #

# carousal component
COMPONENT_CAROUSAL = {TYPE: TEMPLATE, PAYLOAD: {TEMPLATE_TYPE: GENERIC}}

# Subcomponents of the carousal
SUBCOMPONENT_CARD = {
    "default_action": {"type": "", "url": ""},
    "image_url": "",
    "title": "",
    "subtitle": "",
    "buttons": []
}

SUBCOMPONENT_DEFAULT_ACTION_URL = {TYPE: WEB_URL, URL: ""}

SUBCOMPONENT_DEFAULT_ACTION_PAYLOAD = {TYPE: POST_BACK, PAYLOAD: ""}

SUBCOMPONENT_BUTTON_URL = {TITLE: "", TYPE: WEB_URL, URL: ""}

SUBCOMPONENT_BUTTON_PAYLOAD = {TITLE: "", TYPE: POST_BACK, PAYLOAD: ""}

#    ----- ----- ----- ----- ----- ----- ----- Quick Replies ----- ----- ----- ----- ----- ----- ----- ----- -----    #

QR_YES = "Yes"
QR_NO = "No"
QR_STOP = "Stop"
QR_SHOW_MORE_RESTAURANTS = "Show more restaurants"
QR_SEARCH_RESTAURANTS = "Search restaurants"

# ------- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ------ #


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ------------------------------------------ Utterance Templates Constants ------------------------------------------ #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

UTTER_TEMPLATE__RESTAURANT_SUGGESTION = "It Seems you'll like "
UTTER_TEMPLATE__RESTAURANT_SUGGESTION_NOT_FOUND = "your favor not found... I am afraid you said something invalid 😥 "

# ---------------------------------------------------- Utterance Variables ------------------------------------------- #
UTTER_SENTENCE_LIST_FOR_ASKING_TO_MAKE_RESERVATION = [
    "Do you want to book a table at {}?",
    "Are you interested in making a reservation at {}?",
    "Shall I go ahead and book a table for you at {}?",
    "Would you like me to reserve a spot for you at {}?"
]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# -------------------------------------------------- Slot Constants ------------------------------------------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


USER_ID = "user_id"
# CUISINE = "cuisine"
RESTAURANT_ID = "restaurant_id"
RESTAURANT_NAME = "restaurant_name"
SELECTED_RESTAURANT = "selected_restaurant"
NUM_PEOPLE = "num_people"
DATE = "date"
TIME = "time"
PREFERENCES = "preferences"
# CITY = "city"

BOOKING_REFERENCE_ID = "booking_reference_id"

# -------------------------- Knowledge base query related --------------------------
OBJECT_TYPE = "object_type"
MENTION = "mention"
ATTRIBUTE = "attribute"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ------------------------------------------- Restaurant Object Constants ------------------------------------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

ID = "id"
NAME = "name"
CITY = "city"
ADDRESS = "address"
TELEPHONE = "telephone"
CUISINE = "cuisine"
RATINGS = "ratings"
OPENING_HOURS = "opening_hours"
IMAGE_URL = "image_url"
PAGE_URL = "page_url"
MENU_URL = "menu_url"
MON_TO_FRI = "Mon - Fri"
SAT_SUN = "Sat, Sun"

UPCOUNTRY = "Upcountry"
COASTAL = "Coastal"

FIVE_STAR = "⭐️⭐️⭐️⭐️⭐️"
FOUR_STAR = "⭐️⭐️⭐️⭐️️"
THREE_STAR = "⭐️⭐️⭐️"
TWO_STAR = "⭐️⭐️️"
ONE_STAR = "⭐️️"

# Cuisines
CHINESE = "Chinese"
ITALIAN = "Italian"
MEXICAN = "Mexican"
SRI_LANKAN = "Sri Lankan"
THAI = "Thai"

# Categories
# add categories from the dataset

# food taste categories
BITTER = "bitter"
SALTY = "Salty"
SAVORY = "Savory"
SOUR = "Sour"
SPICY = "Spicy"
SWEET = "Sweet"

#
