from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

UserModel= get_user_model()

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields= '__all__'


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'

    def create(self, validated_data):
        user_obj = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
            )
        user_obj.email = validated_data['email']
        user_obj.save()
        return user_obj


class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = '__all__'
    
    username = serializers.CharField()
    password = serializers.CharField()

    def check_user(self, validated_data):
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if not user:
            raise ValueError('User not found')
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'groups', 'status', 'role', 'email', 'last_login')


class UserGroupAddSerializer(serializers.ModelSerializer):

    class Meta:
        model=UserModel
        fields = '__all__'

    def set_user_to_group(self, user_id, group_name):
        user = UserModel.objects.get(pk = user_id)
        group = Group.objects.get(name = group_name)
        user.role = group_name
        user.groups.add(group)
        user.save()    
