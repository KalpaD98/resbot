import logging
import sys

from constants import *

sys.path.append("/Users/kalpafernando/PycharmProjects/resbot/actions/submodules")


# -------------------------- Chat Widget --------------------------------

# -------------------------- BOT-FRONT --------------------------------

# change this according to my needs
def response_generator(criteria_based_restaurant_documents):
    if criteria_based_restaurant_documents and criteria_based_restaurant_documents is not None:
        logging.info("Utils [responseGenerator]:  reformation the responses")

        carousel = COMPONENT_CARROUSAL
        elements_list = []
        for i in criteria_based_restaurant_documents:
            card = {}
            # card[DEFAULT_ACTION] = {TYPE: WEB_URL, URL: i.get(PAGE_URL)}
            # card[IMAGE_URL] = i.get(IMAGE_URL)
            # card[TITLE] = i.get(NAME)
            # card[SUBTITLE] = "Rating " + str(i.get(STARRATE))
            #
            # buttonsList = []
            # button1 = {}
            # button2 = {}
            # button1[URL] = i.get(PAGE_URL)
            # button1[TITLE] = VIEW_PAGE
            # button1[TYPE] = WEB_URL
            # button2[URL] = i.get(MENU)
            # button2[TITLE] = "Menu"
            # button2[TYPE] = WEB_URL
            #
            # buttonsList.append(button1)
            # buttonsList.append(button2)
            #
            # card[BUTTONS] = buttonsList

            elements_list.append(card)
            # SUBCOMPONENT_CARD[]=i.get()
            # SUBCOMPONENT_CARD[]=i.get()
            # SUBCOMPONENT_CARD[]=i.get()
            # SUBCOMPONENT_CARD[]=i.get()

        carousel[PAYLOAD][ELEMENTS] = elements_list
        return carousel
    else:
        logging.error("Utils [responseGenerator]:  FAILED reformating the responses")
        return None


def response_generator_shell(restaurant_documents):
    response_txt = None

    if restaurant_documents is not None and restaurant_documents:
        logging.info("Utils [responseGenerator_Shell]: Hotel Docs FOUND and generating shell response")

        num = 1
        response_txt = ""
        for i in restaurant_documents:
            response_txt = response_txt + str(num) + ". " + i.get("name") + "    "
            num = num + 1
        return response_txt
    else:
        logging.warning("Utils [responseGenerator_Shell]: Hotel Docs NOT FOUND and Fail to genenrate shell response")
        return response_txt


# returns a list of elements in List of list  so as in [[1,2][3,4][5,6]]--->[1,2,3,4,5,6]
def get_total_elements_in_list(list_of_lists):
    if list_of_lists and list_of_lists is not None:
        flat_list = [item for sublist in list_of_lists for item in sublist]
        return flat_list
    else:
        logging.warning("Utils [getTotalElementsInList] : Something Went Wrong in getTotalElementsInList method")
        return None

    # remove duplicate dictionaries from the list

# def responseGenerator(CriteriaBasedHotelDocuments):

#     print("Hii")
# if CriteriaBasedHotelDocuments and CriteriaBasedHotelDocuments is not None:
#     logging.info("Utils [responseGenerator]:  reformating the responses")

#     carousel= COMPONENT_CAROUSAL
#     elementsList=[]
#     for i in CriteriaBasedHotelDocuments:

#         card= SUBCOMPONENT_CARD
#         card[DEFAULT_ACTION]=i.get(PAGE_URL)
#         card[IMAGE_URL]=i.get(IMAGE_URL)
#         card[TITLE]=i.get(NAME)
#         card[SUBTITLE]="Rating "+str(i.get(STARRATE))

#         buttonsList=[]
#         button1=SUBCOMPONENT_BUTTON
#         button1[URL]=i.get(PAGE_URL)
#         button1[TITLE]=VIEW_PAGE
#         button1[TYPE]=WEB_URL

#         buttonsList.append(button1)

#         card[BUTTONS]=buttonsList

#         elementsList.append(card)
#         # SUBCOMPONENT_CARD[]=i.get()
#         # SUBCOMPONENT_CARD[]=i.get()
#         # SUBCOMPONENT_CARD[]=i.get()
#         # SUBCOMPONENT_CARD[]=i.get()


#     carrousal[PAYLOAD][ELEMENTS]= elementsList

# return carrousal
#     {"type":"template","payload":{"template_type":"generic","elements":[
#     {
#     "default_action":{"type":"web_url","url":"https://stackoverflow.com/questions/23368575/pymongo-find-and-modify/23369162"},
#     "image_url":"https://i.imgur.com/nGF1K8f.jpg",
#     "title":"title1",
#     "subtitle":"subtitle1",
#     "buttons":[{"url":"http://donsmaps.com/clickphotos/dolnivi200x100.jpg","title":"Tittletemp"},
#                 {"url":"http://donsmaps.com/clickphotos/dolnivi200x100.jpg","title":"Tittletemp"},
#                ]
#     },
#     {
#     "default_action":"http://donsmaps.com/clickphotos/dolnivi200x100.jpg",
#     "image_url":"https://i.imgur.com/nGF1K8f.jpg",
#     "title":"title1",
#     "subtitle":"subtitle1",
#     "buttons":[{"url":"http://donsmaps.com/clickphotos/dolnivi200x100.jpg","title":"Tittletemp"},
#                 {"url":"http://donsmaps.com/clickphotos/dolnivi200x100.jpg","title":"Tittletemp"},
#                ]
#     },
#     {
#     "default_action":"http://donsmaps.com/clickphotos/dolnivi200x100.jpg",
#     "image_url":"https://i.imgur.com/nGF1K8f.jpg",
#     "title":"title1",
#     "subtitle":"subtitle1",
#     "buttons":[{"url":"https://stackoverflow.com/questions/23368575/pymongo-find-and-modify/23369162","title":"Tittletemp","type":"web_url"},
#                 {"url":"https://stackoverflow.com/questions/23368575/pymongo-find-and-modify/23369162","title":"Tittletemp","type":"web_url"},
#                ]
#     }
# ]}}
