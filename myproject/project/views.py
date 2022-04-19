import pdb

from django.contrib.auth.decorators import login_required
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
from .models import News, Guest, Visitors
from .form import NewsForm

User = get_user_model()


def signup(request):
    try:
        if request.method == "POST":
            name = request.POST['name']
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

            user = User.objects.create_user(email=email, password=password1)
            user.flat = flat
            user.name = name
            user.tower = tower
            user.phone = phone
            user.email = email
            user_otp = random.randint(1000, 9999)
            request.session['email'] = email
            request.session['otp'] = user_otp
            user.is_active = False
            user.save()

            mess = f"Hello {user.email}, \n Your OTP is {user_otp} \n Thank You"

            send_mail(
                "Welcome",
                mess,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
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

        if OTP == int(request.POST['otp']):
            user = User.objects.get(email=request.session['email'])
            user.is_verified = True
            user.is_active = True
            # pdb.set_trace()
            user.save()
            return redirect('project:login')
        else:
            return render(request, 'verify.html', {'error': "OTP does not match. recheck it"})
    return render(request, 'verify.html')


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print(password, "password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            log(request, user)

            return redirect("/project/userdashboard")
        else:
            return render(request, 'login.html', {'error': "Invalid Credentials"})
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
    return redirect('/project/login')


@login_required(login_url='/project/login')
def add_news(request):
    if request.method == "POST":
        form = NewsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()

            return render(request, "add_news.html")
    else:
        form = NewsForm()
    return render(request, "add_news.html", {'form': form})


def guest(request):
    obj = News.objects.filter().order_by('-dateTime')

    return render(request, "guest_dashboard.html", {'news': obj})


def user_dashboard(request):
    obj = News.objects.filter().order_by('-dateTime')
    obj1 = Visitors.objects.filter().order_by('-dateTime')
    return render(request, "user_dashboard.html", {'news': obj, 'visitor': obj1})


def rent(request):
    if request.method == "POST":
        rnt = Guest.objects.create()
        rnt.name = request.POST['name']
        rnt.email = request.POST['email']
        rnt.mobile = request.POST['mobile']
        rnt.flat_size = request.POST['flat_size']
        rnt.flat_type = request.POST['flat_type']
        rnt.member = request.POST['member']
        rnt.pool = request.POST.get('pool')
        rnt.gym = request.POST.get('gym')
        rnt.creche = request.POST.get('creche')
        rnt.flat_rent = True
        rnt.save()
        return redirect('project:message')

    return render(request, "rent.html")


def buy(request):
    if request.method == "POST":
        rnt = Guest.objects.create()
        rnt.name = request.POST.get('name')
        rnt.email = request.POST.get('email')
        rnt.mobile = request.POST.get('mobile')
        rnt.furnished = request.POST.get('furnished')
        rnt.flat_size = request.POST.get('flat_size')
        rnt.flat_buy = True
        rnt.save()
        return redirect('project:message')
    return render(request, "buy.html")


def message(request):
    return render(request, 'message.html')


def resident(request):
    usr = User.objects.filter().order_by('name')
    return render(request, 'resident.html', {'user': usr})


def visitors(request):
    if request.method == "POST":
        vis = Visitors.objects.create()

        vis.name = request.POST['name']
        vis.gender = request.POST['gender']
        vis.mobile = request.POST['mobile']
        vis.place = request.POST['place']
        vis.save()
        return redirect('project:userdashboard')
    return render(request, "visitors.html")
