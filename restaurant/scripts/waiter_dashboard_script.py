import random
from collections import defaultdict

meals_cost = [(random.randint(1, 30) * random.randint(1, 6)) for i in range(10)]

waiter_id = [j + 1 for j in range(5)]


def test_orders():
    list_of_objects = []
    for x in range(30):
        list_of_objects.append({
            "order_id": x + 1,
            "waiter_id": waiter_id[random.randint(0, 4)],
            "meals_cost": meals_cost[random.randint(0, 9)]
        })
    return list_of_objects


test = test_orders()


def sort_key(element):
    return element['waiter_id']


test.sort(key=sort_key)
grouped_list = defaultdict(list)

for item in test:
    grouped_list[item['waiter_id']].append(item)


