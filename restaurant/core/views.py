#django
from django.shortcuts import render
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from waiter.models import Waiter, LogedWaiter

# rest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
# Serializer
from core.serializers import UserLoginSerializer, UserRegisterSerializer, UserSerializer, UserGroupAddSerializer, UserSerializer
# Validation
from core.validations import validate_password, custom_validation, validate_username 

from core.models import AbstractUser, CustomUserManager, CustomUser

class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        clean_data = custom_validation(request.data)
        
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data) 
            print(user)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateWaiterUserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
    
	def post(self, request):
		clean_data = custom_validation(request.data)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid():
			user = serializer.create(clean_data)
			
			get_user = CustomUser.objects.get(email=clean_data['email'])
			group = Group.objects.get(name = "waiters")
			get_user.role = "waiters"
			get_user.groups.add(group)
			get_user.save()

			# add user to waiter table
			waiter = Waiter(user_id = get_user, waiter_name= clean_data['username'])
			waiter.save()	
			# add waiter to login system
			login_waiter = LogedWaiter(waiter_id = waiter, is_logged= False)
			login_waiter.save(0)
			
			return Response('Problem with adding waiter',status=status.HTTP_200_OK)
		
		return Response(status=status.HTTP_400_BAD_REQUEST)
		

#{"username": "testone" , "password":"test1234"}
class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	##
	def post(self, request):
		data = request.data
		assert validate_username(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		username = request.data.get('username')
		password = request.data.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			serializer = UserSerializer(user)
			print(serializer.data)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response({"error": "Login failed"}, status=status.HTTP_400_BAD_REQUEST)

		# if serializer.is_valid(raise_exception=True):
		# 	user = serializer.check_user(data)
		# 	login(request, user)
		# 	print(serializer.return_user_id())
		# 	# get user object by id 

		# 	#return user information
		# 	return Response(serializer.data, status=status.HTTP_200_OK)
        

class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)


""" ADD PERMISIONS ONLY FOR ADMIN / OWNER """

#{ "group": "waiters" , "user_id": 2}
@api_view(['GET'])
def get_all_users(request):
	if request.method == 'GET':
		
		Users = get_user_model()
		all_users = Users.objects.all()
		if all_users:
			serializer = UserSerializer(all_users, many=True)
			return Response(serializer.data)
		return Response({"Error with geting all users"})

@api_view(['GET'])
def get_groups_for_user(request, id_user):
	Users = get_user_model()
	user = Users.objects.get(id=id_user)
	groups = Group.objects.filter(user=user)

	group_info =[]
	for group in groups:
		group_info.append({
			"name": group.name,

		})
	return Response(group_info)

@api_view(['GET'])
def get_user_information(request):
	if request.method == 'GET':
		
		get_users = CustomUser.objects.filter(role="waiters")

		serializer = UserSerializer(get_users,many=True)
		print(get_users)
		return Response(serializer.data)

@api_view(['PUT'])
def change_user_info(request):
	if request.method == 'PUT':
		user_id = request.data['id']

		get_user = CustomUser.objects.get(pk=user_id)
		get_user.loginnumber = request.data['loginnumber']
		get_user.password = request.data['password']
		get_user.save()
		return Response(status=status.HTTP_200_OK)
	
