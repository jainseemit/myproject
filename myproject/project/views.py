import pdb

from django.shortcuts import render

# Create your views here.
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as log, logout
import time
from django.contrib import messages
import random
# from .models import UserOTP
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()



def signup(request):

 try:
    print(request.method == "POST")
    if request.method == "POST":

        email = request.POST['email']
        phone = request.POST['phone']
        flat = request.POST['flat']
        tower = request.POST['tower']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        print(password1)
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html', {'error': "Password does not match"})


        user = User.objects.create_user(email=email,password= password1)
        user.flat = flat
        user.tower = tower
        user.phone = phone
        user.email=email
        user_otp= random.randint(1000,9999)
        request.session['email'] = email
        request.session['otp'] = user_otp
        user.is_active=False
        user.save()
        print(user,user_otp)
        # UserOTP.objects.create(user=user,otp=user_otp)


        mess= f"Hello {user.email}, \n Your OTP is {user_otp} \n Thank You"

        print(user_otp)
        send_mail(
              "Welcome",
               mess,
               settings.EMAIL_HOST_USER,
               [user.email],
               fail_silently= False
                )

        return redirect('project:verify')
 except IntegrityError:
    q = email + ' already exist'
    messages.error(request, q)
 return render(request, "signup.html")


# def otp(request):
#     if request.method == "POST":
#         get_otp = request.POST.get('otp')
#         # if get_otp:
#         #     get_user = request.POST.get('user')
#         #     usr = User.objects.get(username=get_user)
#         #     if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
#         #         return render(request, "login.html")
#         #pdb.set_trace()
#         for key,value in request.session.items():
#             print(key)
#         usr=User.objects.get(email=request.session['email'])
#         print(usr)
#         print(UserOTP.objects.filter(usr))
#         pdb.set_trace()
#         user= UserOTP.objects.filter(usr)
#         if user.user_otp == get_otp:
#             # user=User.objects.get(email=request.POST['email'])
#             # user.save()
#             user.is_active=True
#             user.save()
#             return redirect('project:login')
#         else:
#             return redirect('project:verify')
#             messages.error(request, f'You entered the wrong OTP')
#     return render(request,'verify.html')

def otp(request):
    # OTP = send_otp(request.session['email'])
    OTP = request.session['otp']
    if request.method == "POST":

        # po = Status.objects.latest('id')
        # email = request.session['email']
        # pdb.set_trace()
        if OTP == int(request.POST['otp']):
            user = User.objects.get(email=request.session['email'])
            user.is_verified = True
            user.is_active= True
            # pdb.set_trace()
            user.save()
            return redirect('project:login')
        else:
            messages.error(request, "OTP does not match. recheck or click to resend otp")
            return render(request,'verify.html' ,{'error': "OTP does not match. recheck it"})
    return render(request, 'verify.html')

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print(password,"password")

        user = authenticate(request,email=email, password=password)


        if user is not None:
            log(request,user)
            print('hi')
            messages.success(request, "Successfully Logged In")
            return redirect("/project/userdashboard")
        else:
            return render(request,'login.html',{'error':"Invalid Credentials"})
    return render(request, "login.html")

  # user = request.user
  #
  #   if request.POST:
  #       form = LoginForm(request.POST)
  #       if form.is_valid():
  #           email = request.POST['email']
  #           password = request.POST['password']
  #           user = authenticate(email=email, password=password)
  #           if user:
  #               # here wer are allowing the user to login.
  #               login(request,user)
  #               return redirect('user_login:dashboard')

def Logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/project/login')

def guest(request):
    return render(request,'guest_dashboard.html')


def user_dashboard(request):
    return render(request,'user_dashboard.html')