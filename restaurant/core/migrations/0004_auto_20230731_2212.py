# Generated by Django 4.2 on 2023-07-31 20:12

from django.db import migrations

# Generated by Django 4.2 on 2023-07-31 18:33
from django.contrib.auth.models import User, Group, Permission
from django.db import migrations




def create_groups(apps, schema_migration):
    User = apps.get_model('core', 'CustomUser')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')


    #Meal models

    add_meal =      Permission.objects.get(codename="add_meal")
    delete_meal =   Permission.objects.get(codename="delete_meal")
    change_meal =   Permission.objects.get(codename="change_meal")
    view_meal =     Permission.objects.get(codename="view_meal")

    add_meal_in_category =      Permission.objects.get(codename="add_mealincategory")
    delete_meal_in_category =      Permission.objects.get(codename="delete_mealincategory")
    change_meal_in_category =      Permission.objects.get(codename="change_mealincategory")
    view_meal_in_category =      Permission.objects.get(codename="view_mealincategory")

    add_ingredient =      Permission.objects.get(codename="add_ingredient")
    delete_ingredient =    Permission.objects.get(codename="delete_ingredient")
    change_ingredient =      Permission.objects.get(codename="change_ingredient")
    view_ingredient =      Permission.objects.get(codename="view_ingredient")

    add_category_menu =      Permission.objects.get(codename="add_categorymenu")
    delete_category_menu =   Permission.objects.get(codename="delete_categorymenu")
    change_category_menu =   Permission.objects.get(codename="change_categorymenu")
    view_category_menu =     Permission.objects.get(codename="view_categorymenu")

    # Orders

    add_order =         Permission.objects.get(codename="add_order")
    delete_order =      Permission.objects.get(codename="delete_order")
    change_order =      Permission.objects.get(codename="change_order")
    view_order =        Permission.objects.get(codename="view_order")

    add_ordered_meals    =      Permission.objects.get(codename="add_orderedmeals")
    delete_ordered_meals =   Permission.objects.get(codename="delete_orderedmeals")
    change_ordered_meals =   Permission.objects.get(codename="change_orderedmeals")
    view_ordered_meals   =     Permission.objects.get(codename="view_orderedmeals")

    # Storage

    add_product =                    Permission.objects.get(codename="add_product")
    delete_product =                 Permission.objects.get(codename="delete_product")
    change_product =                 Permission.objects.get(codename="change_product")
    view_product =                   Permission.objects.get(codename="view_product")

    add_product_in_storage =      Permission.objects.get(codename="add_productinstorage")
    delete_product_in_storage =   Permission.objects.get(codename="delete_productinstorage")
    change_product_in_storage =   Permission.objects.get(codename="change_productinstorage")
    view_product_in_storage =     Permission.objects.get(codename="view_productinstorage")

    add_storage =                   Permission.objects.get(codename="add_storage")
    delete_storage =                Permission.objects.get(codename="delete_storage")
    change_storage =                Permission.objects.get(codename="change_storage")
    view_storage =                  Permission.objects.get(codename="view_storage")

    # Kitchen

    add_kitchen_order =      Permission.objects.get(codename="add_kitchenorder")
    delete_kitchen_order =   Permission.objects.get(codename="delete_kitchenorder")
    change_kitchen_order =   Permission.objects.get(codename="change_kitchenorder")
    view_kitchen_order =     Permission.objects.get(codename="view_kitchenorder")
    

    waiter_permissions = [
        #kitchen
        add_kitchen_order,
        #order
        add_order,
        change_order,
        view_order,
        add_ordered_meals,
        delete_ordered_meals,
        change_ordered_meals,
        view_ordered_meals,

    ]

    kitchen_permissions = [
        view_kitchen_order,
        change_kitchen_order
    ]

    manager_permissions = [
        #meals
        add_meal,
        delete_meal,
        change_meal ,
        view_meal ,
        add_meal_in_category , 
        delete_meal_in_category,
        change_meal_in_category,
        view_meal_in_category ,
        add_ingredient,
        delete_ingredient, 
        change_ingredient, 
        view_ingredient, 
        add_category_menu,
        delete_category_menu,   
        change_category_menu,
        view_category_menu,
        #orders
        add_order,       
        delete_order ,     
        change_order ,      
        view_order ,        
        add_ordered_meals,   
        delete_ordered_meals,
        change_ordered_meals,
        view_ordered_meals,
        #storage 
        add_product ,             
        delete_product           ,
        change_product           ,
        view_product            ,
        add_product_in_storage   ,
        delete_product_in_storage ,
        change_product_in_storage ,
        view_product_in_storage ,
        add_storage             ,
        delete_storage          ,
        change_storage          ,
        view_storage            ,
        #Kitchen
        add_kitchen_order ,
        delete_kitchen_order ,
        change_kitchen_order ,
        view_kitchen_order,
    ]

    owner_permissions = [] + manager_permissions


    waiters = Group(name='waiters')
    waiters.save()

    kitchen = Group(name='kitchen')
    kitchen.save()

    manager = Group(name='manager')
    manager.save()

    owner = Group(name='owner')
    owner.save()

    waiters.permissions.set(waiter_permissions)
    kitchen.permissions.set(kitchen_permissions)
    manager.permissions.set(manager_permissions)
    owner.permissions.set(owner_permissions)



    for user in User.objects.all():
        if user.role == 'waiters':
            waiters.user_set.add(user)
        if user.role == 'kitchen':
            kitchen.user_set.add(user)
        if user.role == 'manager':
            manager.user_set.add(user)
        if user.role == 'owner':
            owner.user_set.add(user)





class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_customuser_role'),
    ]

    operations = [
        migrations.RunPython(create_groups)
    ]
