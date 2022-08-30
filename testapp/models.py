from django.db import models
from django.contrib.auth.models import PermissionsMixin,User
from django.contrib.auth.base_user import AbstractBaseUser



# Create your models here.
class UserProfile(models.Model):
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    phone=models.CharField(max_length=15)
    userid=models.CharField(max_length=10)

    def __str__(self):
        return self.email

    

