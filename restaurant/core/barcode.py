import json
import os

class IndexReader:

    def __init__(self, last_shelf, last_vagetable, last_meat, shelf_bar_code, vegetables, meat, ean_order, ean_order_number):
        self.ean_order = ean_order 
        self.ean_order_number = ean_order_number
        self.last_shelf = last_shelf
        self.last_vagetable = last_vagetable
        self.last_meat = last_meat
        self.shelf_bar_code = shelf_bar_code
        self.vegetables = vegetables
        self.meat = meat


    def json_obj(self):
        return json.dumps(self.__dict__)
    
    def change_bar_code_lenght(self, lenght_number, type_shelf):
        if type_shelf == "shelf_bar_code":
            self.shelf_bar_code = lenght_number
            self.save_data_to_json()
        if type_shelf == "vegetables":
            self.vegetables = lenght_number
            self.save_data_to_json()
        if type_shelf == "meat":
            self.meat = lenght_number
            self.save_data_to_json()
    
    def generate_shelf_bar_code(self):
        self.last_shelf += 1
        self.save_data_to_json()
        return self.last_shelf

    def generate_vagetable_bar_code(self):
        self.last_vagetable += 1
        self.save_data_to_json()
        return self.last_vagetable
    
    def generate_meat_bar_code(self):
        self.last_meat += 1
        self.save_data_to_json()
        return self.last_meat
    
    def generate_ean_order_number(self):
        self.ean_order += 1
        self.save_data_to_json()
        return self.ean_order

    def save_data_to_json(self, file_name='E:\\_DJANGO_PROJECTS\\Restaurant_REACT\\backend\\restaurant\\corebar_code.json'):
        json_data = json.dumps(object_index.__dict__)
        with open(file_name, "w") as outfile:
            outfile.write(json_data)

def load_json_file_into_object(file_name='E:\\_DJANGO_PROJECTS\\Restaurant_REACT\\backend\\restaurant\core\\bar_code.json'):
    loaded_file= json.load(open(file_name))
    object_IndexReader = IndexReader(**loaded_file)
    return object_IndexReader

object_index = load_json_file_into_object()

def get_absolute_path(filename):
    return os.path.abspath(filename)

def get_index(type):
    pass

def create_ean_number(item_index):
    number = 0
    return number

def create_ean_image(number):
    image = None
    return image
