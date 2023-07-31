from datetime import datetime


class ProductInMagazine:
    """   """

    def __init__(self, data):
        self.product_date_expired = None
        self.date_added = None
        self.number_of_product = None
        self.product_type = None
        self.id = None
        self.name = None
        self.product_json_object = data
        self.serialize_data()

    def serialize_data(self):
        self.name = self.product_json_object['products']['name']
        self.product_type = self.product_json_object['products']['product_type']
        self.id = self.product_json_object['id']
        self.number_of_product = float(self.product_json_object['number_of_product'])
        self.date_added = self.product_json_object['product_date_added']
        self.product_date_expired = datetime.strptime(self.product_json_object['product_date_expired'], '%Y-%m-%d').date()

    def __dict__(self):
        return {"id":self.id, 
                "product_date_added":self.date_added , 
                "product_date_expired":self.product_date_expired, 
                "number_of_product":self.number_of_product}


class ProductManager:

    def __init__(self, api_data):
        self.api_data = api_data
        self.list_of_products = []
        self.convert_api_data_to_product_obj()
        self.weight_count_number = 0

    def convert_api_data_to_product_obj(self):
        for product in self.api_data:
            self.list_of_products.append(ProductInMagazine(product))

    def sort_object_list_by_date_exp(self):
        self.list_of_products.sort(key=lambda r: r.product_date_expired)

    def get_from_objects_weights_count(self):
        for obj in self.list_of_products:
            self.weight_count_number += obj.number_of_product

    def get_weight_by_date_expired(self, weight_count):
        if weight_count < self.weight_count_number:
            weight = weight_count
            list_of_id_pis = []
            list_of_weight_pis = []
            for obj in self.list_of_products:
                list_of_id_pis.append(obj.id)
                list_of_weight_pis.append(obj.number_of_product)
                if weight <= sum(list_of_weight_pis):
                    return list_of_weight_pis, list_of_id_pis
        else:
            return False

    def remove_weight(self, weight):
        temp_weight = weight
        tuple_list = self.get_weight_by_date_expired(weight)
        weights = tuple_list[0]
        ids = tuple_list[1]
        print(
            f'tuple w {temp_weight} tumple id {tuple_list}'
        )

        for i in range(len(weights)):
            w = weights[i]
            if w <= temp_weight:
                temp_weight -= weights[i]
                weights[i] = 0
            else:
                weights[i] -= temp_weight

        print(
            f'tuple w {temp_weight} tumple id {tuple_list}'
        )
        temp_dict  = []
        for j in range(len(weights)):
            temp_dict.append({"id_product_in_storage":ids[j], "weights":weights[j]})
        return temp_dict

    def make_query_remove(self, tuple):
        """ tuple = weights_list, ids_list"""
        range_list = len(tuple[0])
        list_weights = tuple[0]
        list_ids = tuple[1]
        for i in range(range_list):
            # DO MAGIC QUERY
            print(f'id{list_ids[i]} weights{list_weights[i]}')

    def return_dict_list(self):
        return [obj.__dict__() for obj in self.list_of_products]