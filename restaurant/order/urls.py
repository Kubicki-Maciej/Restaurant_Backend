from django.urls import path
from order.views import create_order, CreateOrderView
urlpatterns = [
    # Order Post
    path('create_order', CreateOrderView.as_view()),
]