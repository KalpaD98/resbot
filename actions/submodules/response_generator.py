import logging
import sys
from actions.submodules.constants import *
sys.path.append("/Users/kalpafernando/PycharmProjects/resbot/actions/submodules")


# ------------------------------------------------ Bot Front Chat Widget -----------------------------------------------

# This class is used to generate the response for the bot front chat widget
class ResponseGenerator:

    # this method has quick_replies_list, message and dispatcher as parameters
    # method is used to generate the quick replies for the bot front chat widget
    @staticmethod
    def quick_replies(quick_replies_list, with_payload=False):
        quick_reply_text_icons = []

        # loop through the quick replies and add them to the quick_reply_text_icons list
        for quick_reply in quick_replies_list:
            if with_payload:
                quick_reply_text_icons.append(
                    {TITLE: quick_reply.get(TITLE), PAYLOAD: quick_reply.get(PAYLOAD)})
            else:
                quick_reply_text_icons.append({TITLE: quick_reply, PAYLOAD: quick_reply})

        return quick_reply_text_icons

    # -----------------------------------------------------------------------------------------------------------------#
    # this method has message, carousal_data,  and dispatcher as parameters
    # method is used to generate an options carousal for the bot front chat widget
    @staticmethod
    def option_carousal(carousal_objects):

        logging.info("Utils [responseGenerator]:  reformation the responses")

        elements_list = []
        carousel = COMPONENT_CAROUSAL

        for carousal_object in carousal_objects:
            card = {DEFAULT_ACTION: carousal_object[DEFAULT_ACTION],
                    IMAGE_URL: carousal_object.get(IMAGE_URL),
                    TITLE: carousal_object.get(TITLE),
                    SUBTITLE: carousal_object.get(SUBTITLE)}

            buttons_list = carousal_object.get(BUTTONS)

            card[BUTTONS] = buttons_list
            elements_list.append(card)

        carousel[PAYLOAD][ELEMENTS] = elements_list

        return carousel

        # Send the carousel using the `template` object

        # < below is the buttons object for the carousal >
        # "buttons": [{"title": carousal_object["button_title"],
        #              "payload": carousal_object["button_payload"]}]})
        # < - Add the quick replies to the response ->

        # If you would like the buttons to also pass entities to the assistant:

        #     utter_greet:
        #     - text: "Hey! Would you like to purchase motor or home insurance?"
        #     buttons:
        #     - title: "Motor insurance"
        #     payload: '/inform{{"insurance":"motor"}}'
        #
        # - title: "Home insurance"
        # payload: '/inform{{"insurance":"home"}}'
    # -----------------------------------------------------------------------------------------------------------------#


########################################################################################################################

class WebResponseGenerator:
    pass

    # webchat UI
    # data_set = []
    #
    # for i in range(len(rest_list)):
    #     data_set.insert(i, rest_list[i])
    #
    # data = {
    #     "payload": 'cardsCarousel',
    #     "data": data_set
    # }
    #
    # dispatcher.utter_message(json_message=data)


########################################################################################################################
class CmdResponseGenerator:
    pass

    ################# commented old code ####################

    # this method has message, carousal_data,  and dispatcher as parameters
    #  method is used to generate an options carousal for the bot front chat widget
    # @staticmethod
    # def option_carousal(message, carousal_objects, dispatcher: CollectingDispatcher):
    #
    #
    #     carousal_data_list = []
    #
    #     # loop through the carousal_objects and add them to the carousal_data_list list.
    #     for carousal_object in carousal_objects:
    #         carousal_data_list.append({TITLE: carousal_object[TITLE].capitalize(),
    #                                    SUBTITLE: carousal_object[SUBTITLE].capitalize(),
    #                                    IMAGE_URL: carousal_object[IMAGE_URL],
    #                                    BUTTONS: carousal_object[BUTTONS]})
    #
    #     dispatcher.utter_message(text=message, quick_replies=carousal_data_list)
    ################# commented old code ####################

#################################### -------- Response Generation Guide -------- #######################################

# Checkout https://rasa.com/docs/rasa/responses/ for more details


########################################## ------ Commented Code ------ ################################################


# PREVIOUS CODE
# for carousal_object in carousal_objects:
#     element = {
#         DEFAULT_ACTION: {TYPE: WEB_URL, URL: carousal_object.get(IMAGE_URL)},
#         TITLE: carousal_object.get(TITLE),
#         SUBTITLE: carousal_object.get(SUBTITLE),
#         IMAGE_URL: carousal_object.get(IMAGE_URL),
#         BUTTONS: carousal_object.get(BUTTONS)
#     }
#     elements_list.append(element)
#
# carousel = COMPONENT_CAROUSAL[PAYLOAD][ELEMENTS] = elements_list

# def response_generator(criteria_based_restaurant_documents):
#     if criteria_based_restaurant_documents and criteria_based_restaurant_documents is not None:
#         logging.info("Utils [responseGenerator]:  reformation the responses")
#
#         carousel = COMPONENT_CARROUSAL
#         elements_list = []
#         for i in criteria_based_restaurant_documents:
#             card = {}
#             # card[DEFAULT_ACTION] = {TYPE: WEB_URL, URL: i.get(PAGE_URL)}
#             # card[IMAGE_URL] = i.get(IMAGE_URL)
#             # card[TITLE] = i.get(NAME)
#             # card[SUBTITLE] = "Rating " + str(i.get(STARRATE))
#             #
#             # buttonsList = []
#             # button1 = {}
#             # button2 = {}
#             # button1[URL] = i.get(PAGE_URL)
#             # button1[TITLE] = VIEW_PAGE
#             # button1[TYPE] = WEB_URL
#             # button2[URL] = i.get(MENU)
#             # button2[TITLE] = "Menu"
#             # button2[TYPE] = WEB_URL
#             #
#             # buttonsList.append(button1)
#             # buttonsList.append(button2)
#             #
#             # card[BUTTONS] = buttonsList
#
#             elements_list.append(card)
#             # SUBCOMPONENT_CARD[]=i.get()
#             # SUBCOMPONENT_CARD[]=i.get()
#             # SUBCOMPONENT_CARD[]=i.get()
#             # SUBCOMPONENT_CARD[]=i.get()
#
#         carousel[PAYLOAD][ELEMENTS] = elements_list
#         return carousel
#     else:
#         logging.error("Utils [responseGenerator]:  FAILED reformating the responses")
#         return None
#
#
# def response_generator_shell(restaurant_documents):
#     response_txt = None
#
#     if restaurant_documents is not None and restaurant_documents:
#         logging.info("Utils [responseGenerator_Shell]: Hotel Docs FOUND and generating shell response")
#
#         num = 1
#         response_txt = ""
#         for i in restaurant_documents:
#             response_txt = response_txt + str(num) + ". " + i.get("name") + "    "
#             num = num + 1
#         return response_txt
#     else:
#         logging.warning("Utils [responseGenerator_Shell]: Hotel Docs NOT FOUND and Fail to genenrate shell response")
#         return response_txt
#
#
# # returns a list of elements in List of list  so as in [[1,2][3,4][5,6]]--->[1,2,3,4,5,6]
# def get_total_elements_in_list(list_of_lists):
#     if list_of_lists and list_of_lists is not None:
#         flat_list = [item for sublist in list_of_lists for item in sublist]
#         return flat_list
#     else:
#         logging.warning("Utils [getTotalElementsInList] : Something Went Wrong in getTotalElementsInList method")
#         return None

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
