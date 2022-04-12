from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

class User(AbstractUser):
    username = None
    email=models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    flat= models.IntegerField(unique=True,default=0)
    tower=models.IntegerField(unique=True,default=0)
    phone=models.IntegerField(unique=True,default=0)
    password1 = models.CharField(max_length=25, default=0)
    password2 = models.CharField(max_length=25, default=0)




    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# class UserOTP(models.Model):
#     user=models.ForeignKey(User, on_delete=models.CASCADE)
#     time_st=models.DateTimeField(auto_now=True)
#     otp=models.SmallIntegerField()
