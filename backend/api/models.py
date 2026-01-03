from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.conf import settings 
from django.utils import timezone


class User(AbstractUser):
    is_seller = models.BooleanField(default=True)
    def __str__(self):
        return self.username

class RentSpace(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='rent_spaces')
    space_type = models.CharField(max_length=200)
    rent = models.IntegerField()
    deposit = models.IntegerField()
    is_occupied=models.BooleanField(default=False)
    country = models.CharField(max_length=100, default='India')
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    street_address = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='rent_spaces/', 
        storage=MediaCloudinaryStorage(),  # ✅ ADD THIS!
        blank=True, null=True
    )
    def __str__(self):
        return f"{self.space_type} - {self.district}"
