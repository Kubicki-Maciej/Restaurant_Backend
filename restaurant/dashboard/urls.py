from django.urls import path
from dashboard.views import get_food_by_date, get_all_waiters_order, get_active_orders, get_kitchen_orders, get_orders_in_progress_and_waiting, get_magazine_stock, check_magazine_stock, get_waiters_status
urlpatterns = [
    path('t', view=get_food_by_date),
    path('a', view=get_all_waiters_order),
    path('x', view=get_active_orders),
    path('y', view=get_kitchen_orders),
    path('s', view=get_orders_in_progress_and_waiting),
    path('get_magazine_stock', view=get_magazine_stock),
    path('check_magazine_stock', view=check_magazine_stock),
    path('get_waiters_status', view=get_waiters_status),
]