import json
import logging
import sys

sys.path.append("/all_actions/submodules")


# ----  -----  -----  -----  -----  ----- JSON Related object utils -----  -----  -----  -----  -----  ---- #
class JSONUtil:

    @staticmethod
    # Convert  Json to a Dictionary
    def json_to_dict(json_data):
        if isinstance(json_data, list):
            dict_list = []
            logging.info("Json obj list to Dictionary list conversion")
            for i in json_data:
                dict_list.append(json.loads(i))
            return dict_list
        if not isinstance(json_data, list):
            logging.info("Json obj  to Dictionary conversion")
            return json.loads(json_data)

    # convert dictionary to Json
    @staticmethod
    def dict_to_json(dict_data):
        if isinstance(dict_data, list):
            logging.info("Dict list to Json list conversion")
            json_list = []
            for i in dict_data:
                json_list.append(json.dumps(i))
            return json_list
        if not isinstance(dict_data, list):
            logging.info("Dict  to Json obj conversion")
            print("No")
            return json.dumps(dict_data)


        # search in a dictionary list and returns the matching criteria included document

    @staticmethod
    def search_document(document_list, criteria_key, criteria_value):
        selected_restaurant_document = next((item for item in document_list if item[criteria_key] == criteria_value),
                                            None)
        print(selected_restaurant_document)
        if selected_restaurant_document is not None:
            return selected_restaurant_document
        else:
            return None

    @staticmethod
    def remove_duplicate_dictionaries_on_restaurant_id(alist):
        rid = "id"

        memo = set()
        res = []
        for sub in alist:

            # testing for already present value
            if sub[rid] not in memo:
                res.append(sub)

                # adding in memo if new value
                memo.add(sub[rid])

        # printing result
        # print("The filtered list : " + str(res))
        return res
