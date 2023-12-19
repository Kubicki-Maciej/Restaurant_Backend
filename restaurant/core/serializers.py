from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import CustomUser
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

    def return_user_id(self):
        return self.id

class UserSerializer(serializers.ModelSerializer):
    groups_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserModel
        fields = ('id','username', 'email', 'groups', 'status', 'role', 'email', 'last_login', 'groups_name', 'loginnumber')

    def get_groups_name(self, obj):
        # user = UserModel.objects.get(id=obj.id)
        groups = Group.objects.filter(user=obj)
        groups_list = []
        for group in groups:
            groups_list.append({"name":group.name})
        return groups_list


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


class WaiterNameSerializer(serializers.ModelSerializer):
    waiter_name = serializers.SerializerMethodField(read_only=True)
    waiter_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ["waiter_id", "waiter_name"]

    def get_waiter_id(self,obj):
        return obj.id
    
    def get_waiter_name(self, obj):
        return obj.username


