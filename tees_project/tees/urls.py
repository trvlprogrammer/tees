from django.urls import path, include
from .api import (
    TeesDataViewset,
    LoginAPI,
    RegisterAPI,
    UserAPI,
    UserProfileViewSet,
    TeesDataListView
)
from rest_framework import routers
from knox import views as knox_views

router = routers.DefaultRouter()
router.register('api/tees', TeesDataViewset, 'TeesData')
router.register('api/profile', UserProfileViewSet, 'Profile')
router.register('api/teeslist', TeesDataListView, 'ListData')


urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register', RegisterAPI.as_view(), name="acc_register"),
    path('api/auth/login', LoginAPI.as_view(), name="knox_login"),
    path('api/auth/user', UserAPI.as_view(), name="detail_user"),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name="knox_logout"),
]


urlpatterns += router.urls
