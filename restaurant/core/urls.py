from django.urls import path    
from core.views import *

urlpatterns = [
    path('register'),
    path('login'),
    path('logout'),
    path('user')
]