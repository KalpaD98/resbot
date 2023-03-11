# response generator Constants
TYPE = "type"
TEMPLATE = "template"
PAYLOAD = "payload"
TEMPLATE_TYPE = "template_type"
GENERIC = "generic"
ELEMENTS = "elements"
DEFAULT_ACTION = "default_action"
WEB_URL = "web_url"
URL = "url"
IMAGE_URL = "image_url"
TITLE = "title"
SUBTITLE = "subtitle"
BUTTONS = "buttons"

#  Used in the Queries
CITY = "city"
CUISINE = "cuisine"

UPCOUNTRY = "Upcountry"
COASTAL = "Coastal"

RATINGS = "ratings"
FIVE_STAR = "FiveStar"
FOUR_STAR = "FourStar"
THREE_STAR = "ThreeStar"
TWO_STAR = "TwoStar"
ONE_STAR = "OneStar"

# Restaurant details
RESTAURANT_URL = "url"
NAME = "name"
RATINGS = "ratings"
MENU = "menu"

# Cuisines categories
CHINESE = "Chinese"
ITALIAN = "Italian"
MEXICAN = "Mexican"
SRI_LANKAN = "Sri Lankan"
THAI = "Thai"

# Categories


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
