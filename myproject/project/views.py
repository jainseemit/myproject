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
from .models import News, Guest, Visitors, Complain, Contact
from .form import NewsForm
from .tasks import send_email_task
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

            return redirect('project:verify')
    except IntegrityError:
        q = email + ' already exist'
        messages.error(request, q)
    return render(request, "signup.html")


def otp(request):
    if request.method == "GET":
        user_otp = random.randint(1000, 9999)
        email = request.session['email']
        request.session['otp'] = user_otp

        send_email_task.delay(email, user_otp)

    else:
        OTP = request.session['otp']

        if OTP == int(request.POST['otp']):
            user = User.objects.get(email=request.session['email'])
            user.is_verified = True
            user.is_active = True
            user.save()
            return redirect('project:login')
        else:
            return render(request, 'verify.html', {'error': "OTP does not match. recheck it or resend it"})

    return render(request, 'verify.html')


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            request.session['uid'] = request.POST['email'] #creating a session key for the current user email
            log(request, user)
            return redirect("/project/userdashboard")
        else:
            return render(request, 'login.html', {'error': "Invalid Credentials"})
    return render(request, "login.html")


def Logout(request):
    logout(request)
    return redirect('/project/login')


def resetpassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        request.session['email'] = email
        try:
            User.objects.get(email=email)
            mess = f"Hello , \n Your reset password link is 'http://127.0.0.1:8000/project/setpassword' \n Thank You"

            send_mail(
                "Welcome",
                mess,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )

            error = 'Please Check You Email'
            return render(request, 'reset_pass.html', {'error': error})
        except User.DoesNotExist:
            error = 'Please enter valid email Thank You'
            return render(request, 'reset_pass.html', {'error': error})
    return render(request, 'reset_pass.html')


def setpassword(request):
    if request.method == "POST":
        email = request.session['email']

        try:
            user = User.objects.get(email=email)
            user.set_password(request.POST.get('password'))
            user.save()
            return redirect('project:login')
        except User.DoesNotExist:
            error = 'User Does Not Exist Please enter valid email Thank You'
            return render(request, 'setpassword.html', {'error': error})
    return render(request, 'setpassword.html')


@login_required(login_url='/project/login')
def add_news(request):
    form = NewsForm()
    if request.method == "POST":
        form = NewsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()

            return redirect("/project/userdashboard/")

    return render(request, "add_news.html", {'form': form})


def guest(request):
    obj = News.objects.filter().order_by('-dateTime')

    return render(request, "guest_dashboard.html", {'news': obj})


def user_dashboard(request):
    obj = News.objects.filter().order_by('-dateTime')
    obj1 = Visitors.objects.filter().order_by('-dateTime')
    if request.session.has_key('uid'):      #checking the key for the session
        return render(request, "user_dashboard.html", {'news': obj, 'visitor': obj1})
    else:
        return redirect('/project/login')



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
    return render(request, 'resident.html', {'users': usr})


def visitors(request):
    if request.method == "POST":
        vis = Visitors.objects.create()  # creating object of Visitor class
        vis.name = request.POST['name']
        vis.gender = request.POST['gender']
        vis.mobile = request.POST['mobile']
        vis.place = request.POST['place']
        vis.save()
        return redirect('project:userdashboard')
    return render(request, "visitors.html")


def complain_user(request):
    if request.method == "POST":
        vis = Complain.objects.create()  # creating object of complain class

        vis.name = request.POST['name']
        vis.email = request.POST['email']
        vis.value = request.POST['value']
        vis.message = request.POST['message']
        vis.save()
        return redirect('project:userdashboard')
    return render(request, "user_dashboard.html")


def complain(request):
    if request.method == "POST":
        vis = Complain.objects.create()  # creating object of complain class

        vis.name = request.POST['name']
        vis.email = request.POST['email']
        vis.value = request.POST['value']
        vis.message = request.POST['message']
        vis.save()
        return redirect('project:guest')
    return render(request, "guest_dashboard.html")


def contact(request):
    if request.method == "POST":
        vis = Contact.objects.create()  # creating object of contact class

        vis.name = request.POST['name']
        vis.email = request.POST['email']
        vis.subject = request.POST['subject']
        vis.message = request.POST['message']
        vis.save()
        return redirect('project:guest')
    return render(request, "guest_dashboard.html")


def contact_user(request):
    if request.method == "POST":
        vis = Contact.objects.create()  # creating object of contact class

        vis.name = request.POST['name']
        vis.email = request.POST['email']
        vis.subject = request.POST['subject']
        vis.message = request.POST['message']
        vis.save()
        return redirect('project:userdashboard')
    return render(request, "user_dashboard.html")
