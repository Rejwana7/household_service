from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from .constants import GENDER_TYPE
from django.db.models import Avg,Count

# Create your models here.
class  ClientAccount(AbstractUser):
    profile_image=models.ImageField(default='media/uploads/default.jpg',upload_to='account/media/uploads',null=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    social_media_links= models.URLField(max_length=250,null=True,blank=True)
    address=models.CharField(max_length=200,null=True,blank=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name}'s profile"
    

    def cart_item_count(self):
        # from services.models import Cart
        
        return self.cart_set.count()
        