import json
from django.test import TestCase, Client
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import TeesData, ProfileUser
from rest_framework.test import APIRequestFactory
from django.urls import include, path, reverse
from .serializers import (
    TeesDataSerializer,
    LoginSerializer,
    RegisterSerializer,
    ProfileUserSerializer,
    UserSerializer,
    TeesDataListSerializer
)
from .api import (
    TeesDataViewset,
    LoginAPI,
    RegisterAPI,
    UserAPI,
    UserProfileViewSet,
    TeesDataListView
)

from rest_framework.test import APITestCase, URLPatternsTestCase
# Create your tests here.


class TeesTestdata(TestCase):
    client = Client()

    def setUp(self):
        self.username = "joji"
        self.email = "joji@mail.com"
        self.password = "joji"

        user = User.objects.create_user(
            self.username, self.email, self.password
        )
        self.user = user

        self.profile = ProfileUser.objects.create(
            name=user.username, owner=user
        )
        self.teesdata1 = TeesData.objects.create(
            name="joji",
            email="joji@mail.com",
            size="lg",
            owner=user
        )
        self.teesdata2 = TeesData.objects.create(
            name="niki",
            email="niki@mail.com",
            size="sm",
            owner=user
        )

        self.login_joji_payload = {
            'username': self.username,
            'password': self.password
        }

        self.valid_payload = {
            'name': 'Brian',
            'email': 'brian@mail.com',
            'size': 'lg',
            'owner': '' + str(user.id)
        }

        self.invalid_payload = {
            'name': '',
            'email': 'manuel@mail.com',
            'size': 10,
            'owner': '' + str(user.id)
        }

        self.content_type = 'application/json'
        login_response = self.client.post(
            reverse('knox_login'),
            data=json.dumps(self.login_joji_payload),
            content_type=self.content_type
        )
        token = login_response.data['token']

        self.Token = 'Token ' + str(token)

    def test_tees_data(self):
        joji = TeesData.objects.get(name="joji")
        niki = TeesData.objects.get(name="niki")

        self.assertEqual(joji.email, "joji@mail.com")
        self.assertEqual(joji.size, "lg")
        self.assertEqual(niki.email, "niki@mail.com")
        self.assertEqual(niki.size, "sm")

        print("test was successfull>>>>>>>>")

    def test_get_all_tees_data(self):
        url = reverse('ListData-list')
        response = self.client.get(url, format='json')
        data_list = TeesData.objects.all()
        serializer = TeesDataListSerializer(data_list, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        print("test get all data list was successfull >>>>>>>>>")

    def test_post_data_tees(self):

        valid_response = self.client.post(
            reverse('TeesData-list'),
            data=json.dumps(self.valid_payload),
            content_type=self.content_type,
            HTTP_AUTHORIZATION=self.Token)
        self.assertEqual(valid_response.status_code, status.HTTP_201_CREATED)
        print("post valid " + str(valid_response.status_code))

        invalid_response = self.client.post(
            reverse('TeesData-list'),
            data=json.dumps(self.invalid_payload),
            content_type=self.content_type,
            HTTP_AUTHORIZATION=self.Token
        )
        self.assertEqual(invalid_response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        print("post invalid " + str(invalid_response.status_code))
        print("post test successfull >>>>>>>>>>>>>>>>")

    def test_update_data_tees(self):

        valid_response = self.client.put(
            reverse('TeesData-detail', kwargs={'pk': self.teesdata1.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json', HTTP_AUTHORIZATION=self.Token
        )
        self.assertEqual(valid_response.status_code,
                         status.HTTP_200_OK)

        print("valid update  " + str(valid_response.status_code))

        invalid_response = self.client.put(
            reverse('TeesData-detail', kwargs={'pk': self.teesdata1.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json', HTTP_AUTHORIZATION=self.Token
        )
        self.assertEqual(invalid_response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        print("invalid update  " + str(invalid_response.status_code))

        profile_response = self.client.put(
            reverse('Profile-detail', kwargs={'pk': self.profile.id}),
            data=json.dumps({'name': 'new name'}),
            content_type='application/json', HTTP_AUTHORIZATION=self.Token
        )
        print(profile_response.status_code)
        self.assertEqual(profile_response.status_code,
                         status.HTTP_200_OK)
        print("profile update  " + str(profile_response.status_code))

        print("update test was successfull")

    def test_delete_tees_data(self):

        valid_response = self.client.delete(
            reverse('TeesData-detail', kwargs={'pk': self.teesdata1.pk}),
            content_type='application/json', HTTP_AUTHORIZATION=self.Token
        )
        self.assertEqual(valid_response.status_code,
                         status.HTTP_204_NO_CONTENT)

        print("valid delete  " + str(valid_response.status_code))

        invalid_response = self.client.delete(
            reverse('TeesData-detail', kwargs={'pk': 20}),
            content_type='application/json', HTTP_AUTHORIZATION=self.Token
        )
        self.assertEqual(invalid_response.status_code,
                         status.HTTP_404_NOT_FOUND)

        print("invalid delete  " + str(invalid_response.status_code))
