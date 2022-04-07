from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


from django.contrib import messages
import random
from .models import UserOTP
from django.core.mail import send_mail
from django.conf import settings



def Register(request):
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        flat = request.POST['flat']
        tower = request.POST['tower']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/signup')

        user = User.objects.create_user(email, password1)
        user.flat = flat
        user.tower = tower
        user.phone = phone
        user.email=email
        user.save()
        user_otp= random.randint(10000,99999)
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

        return render(request, 'verify.html',{'otp' :True, 'user': user})
    return render(request, "signup.html")


def otp(request):
    if request.method == "POST":
        get_otp = request.POST.get('otp')
        if get_otp:
            get_user = request.POST.get('user')
            usr = User.objects.get(username=get_user)
            if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                return render(request, "login.html")
            else:
                    messages.error(request, f'You entered the wrong OTP')
