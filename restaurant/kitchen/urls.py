from django.urls import path
from kitchen.views import get_kitchen_orders_inprogress, test_kitchen_orders, is_done_kitchen_order, in_progress_kitchen_order

urlpatterns = [
    path('orders/', view=get_kitchen_orders_inprogress,
        name='get_all_kitchen_orders'),
    path('get_orders/', view=test_kitchen_orders,
        name='TEST'),
    path('change_order_in_progress/<int:id>',
        view=in_progress_kitchen_order),
    path('change_order_done/<int:id>',
        view=is_done_kitchen_order),
]