from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

app_name = 'project'
urlpatterns = [
    path("guest/", views.guest, name="guest"),
    path("userdashboard/", views.user_dashboard, name="userdashboard"),
    path("signup/", views.signup, name="signup"),
    path('verify/', views.otp, name='verify'),
    path("login/", views.login, name="login"),
    path("add_news/", views.add_news, name="add_news"),
    path("visitors/", views.visitors, name="visitors"),
    path("complain/", views.complain, name="complain"),
    path("complain/", views.complain_user, name="complainuser"),
    path("contact/", views.contact_user, name="contactuser"),
    path("contact/", views.contact, name="contact"),

    path("rent/", views.rent, name="rent"),
    path("buy/", views.buy, name="buy"),
    path("resident/", views.resident, name="resident"),
    path("message/", views.message, name="message"),

    path("resetpassword/", views.resetpassword, name="resetpassword"),
    path("setpassword/", views.setpassword, name="setpassword"),



    path("logout/", views.Logout, name="logout"),
]
