from django.db import models
from account.models import ClientAccount
# Create your models here.

class ContactUs(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField()
    subject=models.TextField()
