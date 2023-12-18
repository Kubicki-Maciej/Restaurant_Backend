from django.urls import path    
from core.views import *

urlpatterns = [
	path('register', UserRegister.as_view(), name='register'),
	path('login', UserLogin.as_view(), name='login'),
	path('logout', UserLogout.as_view(), name='logout'),
	path('user', UserView.as_view(), name='user'),
	path('register_waiter', CreateWaiterUserRegister.as_view(), name='waiter_register'),
    # path('set_to_group', view=set_user_to_group, name="group waiters"),
    path('all_users', view=get_all_users, name="get_all_users"),
    path('get_user/<int:id_user>', view=get_groups_for_user, name="get_groups_for_user")   
]