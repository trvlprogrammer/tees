import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import TeesData, ProfileUser
from ..serializers import (
    TeesDataSerializer,
    LoginSerializer,
    RegisterSerializer,
    ProfileUserSerializer,
    UserSerializer,
    TeesDataListSerializer
)


client = Client()
