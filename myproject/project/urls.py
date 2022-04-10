


from django.urls import path

from . import views


app_name='project'
urlpatterns = [
    path("guest/", views.guest, name="guest"),
    path("signup/", views.signup, name="signup"),
    path('verify/', views.otp, name='verify'),
    path("login/", views.login, name="login"),
    # path("logout/", views.Logout, name="logout"),
]