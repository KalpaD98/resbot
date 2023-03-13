# response generator Constants
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
IMAGE_URL = "image_url"
PAGE_URL = "page_url"
TITLE = "title"
SUBTITLE = "subtitle"
BUTTONS = "buttons"

# Restaurant Constants
ID = "id"

#  Used in the Queries
CITY = "city"
CUISINE = "cuisine"

UPCOUNTRY = "Upcountry"
COASTAL = "Coastal"

RATINGS = "ratings"
FIVE_STAR = "⭐️⭐️⭐️⭐️⭐️"
FOUR_STAR = "⭐️⭐️⭐️⭐️️"
THREE_STAR = "⭐️⭐️⭐️"
TWO_STAR = "⭐️⭐️️"
ONE_STAR = "⭐️️"

# Restaurant details
RESTAURANT_URL = "url"
NAME = "name"
MENU = "menu"

# Cuisines categories
CHINESE = "Chinese"
ITALIAN = "Italian"
MEXICAN = "Mexican"
SRI_LANKAN = "Sri Lankan"
THAI = "Thai"

# Categories
# add categories from the dataset

# Components
COMPONENT_CAROUSAL = {TYPE: TEMPLATE, PAYLOAD: {TEMPLATE_TYPE: GENERIC}}
SUBCOMPONENT_CARD = {
    "default_action": {"type": "", "url": ""},
    "image_url": "",
    "title": "",
    "subtitle": "",
    "buttons": []
}

SUBCOMPONENT_BUTTON = {"url": "", "title": "", "type": ""}

# Utterance Templates
RESTAURANT__SUGGESTION_UTTER_TEMPLATE = "It Seems you'll like "
RESTAURANT_SUGGESTION_NOT_FOUND_UTTER_TEMPLATE = "your favor not found... I am afraid you said something invalid 😥 "

# food taste categories
BITTER = "bitter"
SALTY = "Salty"
SAVORY = "Savory"
SOUR = "Sour"
SPICY = "Spicy"
SWEET = "Sweet"
