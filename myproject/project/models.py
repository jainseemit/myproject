from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=100, default=0)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    flat = models.IntegerField(unique=True, default=0)
    tower = models.IntegerField(unique=True, default=0)
    phone = models.IntegerField(unique=True, default=0)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


# class UserOTP(models.Model):
#     user=models.ForeignKey(User, on_delete=models.CASCADE)
#     time_st=models.DateTimeField(auto_now=True)
#     otp=models.SmallIntegerField()

class News(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    dateTime = models.DateTimeField(auto_now_add=True)


class Guest(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=False)
    mobile = models.CharField(max_length=14)
    flat_buy = models.BooleanField(default=False)
    flat_rent = models.BooleanField(default=False)
    furnished = models.CharField(max_length=100)
    pool = models.BooleanField(null=True)
    gym = models.BooleanField(null=True)
    creche = models.BooleanField(null=True)
    member = models.IntegerField(default=0)
    flat_size = models.CharField(max_length=20)


class Visitors(models.Model):
    name = models.CharField(max_length=50, default='none')
    gender = models.CharField(max_length=25)
    mobile = models.IntegerField(default=0)
    place = models.CharField(max_length=100, default='none')
    dateTime = models.DateTimeField(auto_now_add=True, null=True)


class Complain(models.Model):
    name = models.CharField(max_length=50, default='none')
    email = models.EmailField(max_length=25)
    value = models.CharField(null=True,max_length=25)
    message = models.TextField(max_length=1000, default='none')

class Contact(models.Model):
    name = models.CharField(max_length=50, default='none')
    email = models.EmailField(max_length=25)
    subject = models.CharField(null=True,max_length=100)
    message = models.TextField(max_length=1000, default='none')

