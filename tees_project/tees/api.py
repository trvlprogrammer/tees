from tees.models import TeesData, ProfileUser
from rest_framework import permissions, viewsets, generics
from knox.models import AuthToken
from rest_framework.response import Response
# from knox.auth import TokenAuthentication
from django.contrib.auth.models import User
from .serializers import (
    TeesDataSerializer,
    LoginSerializer,
    RegisterSerializer,
    ProfileUserSerializer,
    UserSerializer,
    TeesDataListSerializer
)


class TeesDataViewset(viewsets.ModelViewSet):

    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = TeesDataSerializer

    def get_queryset(self):
        return TeesData.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):

        serializer.save(owner=self.request.user)


class TeesDataListView(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    serializer_class = TeesDataListSerializer

    queryset = TeesData.objects.all()


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = ProfileUserSerializer

    def get_queryset(self):
        return ProfileUser.objects.filter(owner=self.request.user)
