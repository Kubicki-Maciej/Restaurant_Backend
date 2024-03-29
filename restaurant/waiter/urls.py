from django.urls import path
from waiter.views import create_waiter_order, get_all_waiter_orders, get_all_waiter_orders_active, get_all_waiter_history_orders, get_waiters_orders

urlpatterns = [
    path('create_waiter_order', view=create_waiter_order),
    path('get_all_waiter_orders', view=get_all_waiter_orders),
    path('get_all_waiter_orders_active', view=get_all_waiter_orders_active),
    path('get_all_waiter_history_orders', view=get_all_waiter_history_orders),
    path('get_waiters_orders', view=get_waiters_orders),
]