from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("dashboard/", views.Dashboard, name="dashboard"),
    path("send_sms_code/", views.send_sms_code, name="send_sms_code"),
]