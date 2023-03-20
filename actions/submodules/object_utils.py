class ObjectUtil:
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
