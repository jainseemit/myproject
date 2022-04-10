import pdb

from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user
import time
from django.contrib import messages
import random
from .models import UserOTP
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()



def signup(request):
    print('Hi')
    print(request.method == "POST")
    if request.method == "POST":
        print('HIiiiiiiiiiiiiiiiiii')
        email = request.POST['email']
        phone = request.POST['phone']
        flat = request.POST['flat']
        tower = request.POST['tower']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html', {'error': "Password does not match"})


        user = User.objects.create_user(email, password1)
        user.flat = flat
        user.tower = tower
        user.phone = phone
        user.email=email
        user_otp= random.randint(1000,9999)
        user.save()
        print(user,user_otp)
        UserOTP.objects.create(user=user,otp=user_otp)


        mess= f"Hello {user.email}, \n Your OTP is {user_otp} \n Thank You"

        print(user_otp)
        send_mail(
              "Welcome",
               mess,
               settings.EMAIL_HOST_USER,
               [user.email],
               fail_silently= False
                )
        request.session['email']=email
        print(email)
        return redirect('project:verify')
    return render(request, "signup.html")


def otp(request):
    if request.method == "POST":
        get_otp = request.POST.get('otp')
        # if get_otp:
        #     get_user = request.POST.get('user')
        #     usr = User.objects.get(username=get_user)
        #     if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
        #         return render(request, "login.html")
        #pdb.set_trace()
        for key,value in request.session.items():
            print(key)
        usr=User.objects.get(email=request.session['email'])
        print(usr)
        user= UserOTP.objects.get(usr)
        if user.user_otp == get_otp:
            # user=User.objects.get(email=request.POST['email'])
            # user.save()
            return redirect('project:login')
        else:
            messages.error(request, f'You entered the wrong OTP')
    return render(request,'verify.html')


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)

        if email is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/home/homes/")
        else:
            return render(request,'login.html',{'error':"Invalid Credentials"})
    return render(request, "login.html")

def guest(request):
    return render(request,'guest_dashboard.html')