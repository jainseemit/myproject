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
    path("password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path("logout/", views.Logout, name="logout"),
]
