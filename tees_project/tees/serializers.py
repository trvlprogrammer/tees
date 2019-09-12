from rest_framework import serializers
from .models import TeesData, ProfileUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class TeesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeesData
        fields = '__all__'


class TeesDataListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeesData
        fields = '__all__'


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])

        ProfileUser.objects.create(owner=user, name=user.username)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
