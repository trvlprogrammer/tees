from django.db import models
from django.contrib.auth.models import User


class TeesData(models.Model):

    small = 'sm'
    medium = 'md'
    large = 'lg'
    extra_large = 'xl'

    t_shirt_size = [
        (small, 'SMALL'),
        (medium, 'MEDIUM'),
        (large, 'LARGE'),
        (extra_large, 'EXTRA LARGE'),
    ]

    name = models.CharField(max_length=150,)
    email = models.EmailField(max_length=150,)
    size = models.CharField(
        max_length=50, choices=t_shirt_size, default=small, blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True,  blank=True)
    # def perform_create(self, serializer):

    #     serializer.save(owner=self.request.user, event_status=True)


class ProfileUser(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True,  blank=True)
    name = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to="profile_picture", blank=True)
