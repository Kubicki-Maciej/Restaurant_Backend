#django
from django.shortcuts import render
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import Group

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

from core.models import AbstractUser, CustomUserManager

class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	##
	def post(self, request):
		data = request.data
		assert validate_username(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			login(request, user)
			return Response(serializer.data, status=status.HTTP_200_OK)
        

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

@api_view(['POST'])	
def set_user_to_group(request):
    if request.method == 'POST':
        data= request.data
        group_name = data['group']
        user_object_id = data['user_id']
        serializer = UserGroupAddSerializer(data=data)
        serializer.set_user_to_group(user_object_id, group_name)

        return Response({f'Użytkownik {user_object_id} dodany do grupy {group_name}'})
    
    return Response({'Something went wrong'})


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