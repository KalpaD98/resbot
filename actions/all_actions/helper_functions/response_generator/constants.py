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
IMAGE_URL = "image_url"
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

#    ----- ----- ----- ----- ----- ----- ----- Quick Replies English ----- ----- ----- ----- ----- ----- ----- -----   #

QR_YES = "Yes"
QR_NO = "No"

QR_HI = "Hi"

QR_STOP = "Stop"

QR_SHOW_MORE_RESTAURANTS = "Show more restaurants"
QR_SEARCH_RESTAURANTS = "Search restaurants"

# ------- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ------ #
