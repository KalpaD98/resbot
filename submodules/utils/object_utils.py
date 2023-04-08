import datetime
import random
import sys

from submodules.constants.constants import *

sys.path.append("/all_actions/submodules")


class ObjectUtils:
    @staticmethod
    def find_by_id(item_id, item_list):
        for item in item_list:
            if item['id'] == item_id:
                return item

    @staticmethod
    def delete_by_id(item_id, item_list):

        for item in item_list:

            if item['id'] == item_id:
                item_list.remove(item)

    @staticmethod
    def delete_by_ids(self, item_ids, item_list):
        list_copy = item_list.copy()
        for item_id in item_ids:
            self.deletebyid(item_id, list_copy)
        return list_copy

    @staticmethod
    def get_all_ids(item_list):
        ids = []
        for item in item_list:
            ids.append(item['id'])
        return ids

    @staticmethod
    def get_random_sentence(object_name, sentences):
        random_sentence = random.choice(sentences)
        return random_sentence.format(object_name)

    # bookings related
    @staticmethod
    def filter_and_format_bookings(bookings):
        today = datetime.date.today()
        filtered_bookings = []

        for booking in bookings:
            booking_date = datetime.datetime.strptime(booking["booking_date"], "%Y-%m-%d").date()
            if booking_date >= today:
                days_remaining = (booking_date - today).days
                booking["days_remaining"] = days_remaining
                filtered_bookings.append(booking)

        return filtered_bookings

    # print '*' in a line when the number of stars given
    @staticmethod
    def star_print(stars):
        print("*" * stars)
