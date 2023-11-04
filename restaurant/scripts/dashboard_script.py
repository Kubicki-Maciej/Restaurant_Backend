import random
import datetime

name_of_meal = [
    'Yorkshire Pudding',
    'Fish and Chips',
    'English Pancakes',
    'Shepherds Pie' ,
    'Black Pudding',
    'Trifle',
    'Full English Breakfas',
    'Toad in the',
]

def random_date_time_str():
    date = f'2023-09-{random.randint(1,30)} {random.randint(9,22)}:{random.randint(1,60)}:00'
    return date

def create_object_meal_list():
    dictionary_meals = {'meals':[]}
    for index in range(len(name_of_meal)):
        dictionary_meals['meals'].append({
            "id":index+1,
            "meal_name":name_of_meal[index],
            "cost":format(((index+1)*2.99),'.2f'),
        })
    return dictionary_meals

object_meals = create_object_meal_list()

def random_order_meals(max_ordered_meals):
    index_used = []
    meals_orderd = []
    for i in range(max_ordered_meals):
        index = random.randint(1,(len(object_meals['meals'])))
        if index not in index_used:
            index_used.append(index)
            amount_of_dish = random.randint(1,5)
            targeted_object_meal = object_meals['meals'][(index-1)]
            temp_dict = {
                "meal":targeted_object_meal,
                "number_of_meal": amount_of_dish
            }
            meals_orderd.append(temp_dict)
        # else skip

    return meals_orderd

def create_list_of_order():
    orders = []
    for index in range(500):
        waiter_id = random.randint(1,5)  
        order_template = {
            "id": index+1,
            "waiter_id": waiter_id,
            "meals_ordered": random_order_meals(random.randint(1,5)),
            "date_end": random_date_time_str()
        }

        orders.append(order_template)
    return orders

def random_date_time():
    date_format = '%Y-%m-%d %H:%M:%S'
    date = f'2023-09-{random.randint(1,30)} {random.randint(9,20)}:{random.randint(1,60)}:00'
    date_obj = datetime.datetime.strptime(date, date_format)
    return date_obj


test_order_list = create_list_of_order()
import json
json_object = json.dumps(test_order_list, indent=4)

# Writing to sample.json
with open("sample.json", "w") as outfile:
    outfile.write(json_object)