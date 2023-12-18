from django.urls import path
from order.views import create_order, update_order, end_order, CreateOrderView
urlpatterns = [
    # Order Post
    path('create_order', CreateOrderView.as_view()),
    path('update_order', view=update_order),
    path('end_order', view=end_order),
    # path('get_waiters_orders', view=get_waiters_orders),

]