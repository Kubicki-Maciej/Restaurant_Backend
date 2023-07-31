from storage.models import Product, ProductInStorage, Storage
from meals.models import Meal, MealInCategory, Ingredient, CategoryMenu
from order.models import Order, OrderedMeals
from core.models import CustomUser
from kitchen.models import KitchenOrder
from core.barcode import object_index


def create_simple_test_db():
    """
    😍😭👍❤️🦮
    """



    user = CustomUser.objects.get(pk=1)

    #create order ean creator
    index_class = object_index
    # Storage section 
    #Products bulk_create()
    #create ean generator for python 
    avocado = Product(name="avocado", product_type="KG")
    bread = Product(name="bread", product_type="P")
    tomato = Product(name="tomato", product_type="KG")
    potato = Product(name="potato", product_type="KG")
    onion = Product(name="onion", product_type="KG")
    cheese = Product(name="cheese", product_type="KG") 
    beef_meat = Product(name="beef_meat", product_type="KG") 
    ground_beef = Product(name="ground_beef", product_type="KG")
    chicken_breast = Product(name="chicken_breast", product_type="KG")
    list_of_product = [
        avocado,
        bread,
        tomato ,
        potato ,
        onion ,
        cheese ,
        beef_meat ,
        ground_beef , 
        chicken_breast
    ]
    for o in list_of_product:
        o.save()
    
    # Product.objects.bulk_create(list_of_product)

    #Storage
    fridge_meat_storage = Storage(name="fridge_meat_storage")
    fridge_vegetables_storage = Storage(name="fridge_vegetables_storage")
    vegetable_storage = Storage(name="vegetable_storage_container")
    bread_storage = Storage(name="bread_storage")
    list_of_storages = [
        fridge_meat_storage,
        fridge_vegetables_storage,
        vegetable_storage,
        bread_storage
    ]
    for o in list_of_storages:
        o.save()
    # Storage.objects.bulk_create(list_of_storages)
    # Product In Storage

    product_a = ProductInStorage(product_id=potato, storage_id=vegetable_storage, number_of_product = 20, product_date_expired='2024-10-10') 
    product_b = ProductInStorage(product_id=potato,storage_id= vegetable_storage, number_of_product = 15, product_date_expired='2024-10-10')
    product_c = ProductInStorage(product_id=onion, storage_id=vegetable_storage, number_of_product = 10, product_date_expired='2024-10-10')
    product_d = ProductInStorage(product_id=bread,storage_id= bread_storage, number_of_product = 5, product_date_expired='2024-10-10')
    product_e = ProductInStorage(product_id=ground_beef, storage_id=fridge_meat_storage, number_of_product = 5, product_date_expired='2024-10-10')
    product_f = ProductInStorage(product_id=cheese,storage_id= fridge_meat_storage, number_of_product = 5, product_date_expired='2024-10-10')

    list_product_in_storage = [
        product_a,
        product_b,
        product_c,
        product_d,
        product_e,
        product_f
    ]

    #ProductInStorage.objects.bulk_create(list_product_in_storage)

    for o in list_product_in_storage:
        o.save()

    #Meals Section

    fries = Meal(meal_name="Fries", meal_cost=9.99, description="Potato choped into long blocks")
    fries_ingredient = Ingredient(product_id=potato,meal_id= fries,weight_pices_used= 0.450)

    cheese_fries = Meal(meal_name="Fries with cheese",meal_cost=13.99,description= "Potato choped into long blocks with cheese")
    fries_ingredient_potato = Ingredient(product_id=potato,meal_id= fries, weight_pices_used=0.450)
    fries_ingredient_cheese = Ingredient(product_id=cheese,meal_id= fries, weight_pices_used=0.150)
    
    burger = Meal(meal_name="Burger", meal_cost=22.49,description= "Ground beef meat with tomato, cheese,onion and bread")
    burger_ingredient_meat = Ingredient(product_id=ground_beef,meal_id= burger,weight_pices_used= 0.300)
    burger_ingredient_tomato = Ingredient(product_id=tomato,meal_id= burger, weight_pices_used=0.050)
    burger_ingredient_cheese = Ingredient(product_id=cheese,meal_id= burger,weight_pices_used= 0.020)
    burger_ingredient_onion = Ingredient(product_id=onion,meal_id= burger,weight_pices_used= 0.020)
    burger_ingredient_bread = Ingredient(product_id=bread,meal_id= burger,weight_pices_used= 0.100)
    
    hamburger = Meal(meal_name="Burger", meal_cost=17.49,description= "Ground beef and bread")
    hamburger_ingredient_meat = Ingredient(product_id=ground_beef,meal_id= hamburger,weight_pices_used= 0.300)
    hamburger_ingredient_bread = Ingredient(product_id=bread, meal_id=hamburger, weight_pices_used= 0.100)

    chikenburger = Meal(meal_name="Chiken Burger", meal_cost=19.99,description= "Chikenburger with cheese, tomato and bread")
    chikenburger_ingredient_meat = Ingredient(product_id=chicken_breast,meal_id= chikenburger,weight_pices_used=0.300)
    chikenburger_ingredient_tomato = Ingredient(product_id=tomato,meal_id= chikenburger,weight_pices_used= 0.020)
    chikenburger_ingredient_cheese = Ingredient(product_id=cheese, meal_id=chikenburger,weight_pices_used= 0.020)
    chikenburger_ingredient_bread= Ingredient(product_id=bread, meal_id=chikenburger, weight_pices_used=0.100)

    list_of_meal = [
        fries,
        cheese_fries,
        burger,
        hamburger,
        chikenburger,
    ]
    #Meal.objects.bulk_create(list_of_meal)
    for o in list_of_meal:
        o.save()


    list_of_ingredient = [
        burger_ingredient_meat,
        burger_ingredient_tomato,
        burger_ingredient_cheese,
        burger_ingredient_onion ,
        burger_ingredient_bread ,
        fries_ingredient,
        fries_ingredient_potato,
        fries_ingredient_cheese,
        hamburger_ingredient_meat,
        hamburger_ingredient_bread,
        chikenburger_ingredient_meat ,
        chikenburger_ingredient_tomato,
        chikenburger_ingredient_cheese,
        chikenburger_ingredient_bread,
    ]
    for o in list_of_ingredient:
        o.save()

    # Ingredient.objects.bulk_create(list_of_ingredient)

    
    # categories 

    starters_categorty = CategoryMenu(category_name="Starters", category_explenation="small dishes always first to serve")
    burger_categorty = CategoryMenu(category_name="Burgers", category_explenation="all burgers")
    
    list_of_categorys = [
        starters_categorty,
        burger_categorty
    ]
    for o in list_of_categorys:
        o.save()

    # CategoryMenu.objects.bulk_create(list_of_categorys)

    #meal into category 

    burger_in_category = MealInCategory(meal_id=burger, category_menu_id=burger_categorty)
    hamburger_in_category = MealInCategory(meal_id=hamburger,category_menu_id= burger_categorty)
    burgerchiken_in_category = MealInCategory(meal_id=chikenburger,category_menu_id= burger_categorty)

    fries_in_category = MealInCategory(meal_id = fries, category_menu_id=starters_categorty)
    fries_in_category = MealInCategory(meal_id = cheese_fries, category_menu_id=starters_categorty)

    list_of_meal_in_categories = [
        burger_in_category,
        hamburger_in_category,
        burgerchiken_in_category,
        fries_in_category,
        fries_in_category,
    ]

    for o in list_of_meal_in_categories:
        o.save()
    # MealInCategory.objects.bulk_create(list_of_meal_in_categories)




    # !DO TABLE MODEL!
    ean_order = index_class.generate_ean_order_number()
    order_one = Order(user_id=user, table_id=25, ean_code= ean_order, generated_code=str(ean_order))

    list_of_order = [
        order_one
    ]
        
    for o in list_of_order:
        o.save()
    #Order.objects.bulk_create(list_of_order)

    order_one_fries = OrderedMeals(order_id=order_one, meal_id=fries, number_of_meals=2, comments= "more salt")
    order_one_burger = OrderedMeals(order_id=order_one, meal_id=burger, number_of_meals=1, comments="")
    order_one_hamburger = OrderedMeals(order_id=order_one, meal_id=hamburger, number_of_meals=1, comments="")

    list_of_ordered_meals = [
        order_one_burger,
        order_one_fries,
        order_one_hamburger
    ]
        
    for o in list_of_ordered_meals:
        o.save()
        
    #OrderedMeals.objects.bulk_create(list_of_ordered_meals)

    kitchen_order_one = KitchenOrder(order_id=order_one)
    list_kitchen_order = [kitchen_order_one]
        
    for o in list_kitchen_order:
        o.save()

    #KitchenOrder.objects.bulk_create(list_kitchen_order)

def create_order():
    index_class = object_index

    user = CustomUser.objects.get(pk=1)
    ean_order = index_class.generate_ean_order_number()

    order = Order(user_id=user, table_id=26, ean_code= ean_order, generated_code=str(ean_order))

    list_of_order = [
        order
    ]

    for o in list_of_order:
        o.save()

    # Order.objects.bulk_create(list_of_order)
    fries = Meal.objects.get(meal_name="Fries with cheese")
    burger = Meal.objects.get(meal_name="Chiken Burger")

    order_fries = OrderedMeals(order_id=order, meal_id=fries, number_of_meals=2, comments= "please more cheese")
    order_burger = OrderedMeals(order_id=order, meal_id=burger, number_of_meals=4, comments="rare +")
    

    list_of_ordered_meals = [
        order_fries,
        order_burger,
    ]
        
    for o in list_of_ordered_meals:
        o.save()

    # OrderedMeals.objects.bulk_create(list_of_ordered_meals)

    kitchen_order = KitchenOrder(order_id=order)
    list_kitchen_order = [kitchen_order]
        
    for o in list_kitchen_order:
        o.save()
    
    # KitchenOrder.objects.bulk_create(list_kitchen_order)

print('work')
# create_simple_test_db()


# for i in range(5):
#     print(i)
#     create_order()

print('done')