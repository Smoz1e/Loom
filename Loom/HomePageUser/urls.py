from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from RegAndAuth.views import *

urlpatterns = [
    path("profile/", views.HomePageUser, name="profile"),
    path("profile/upload-avatar/", views.upload_avatar, name="upload_avatar"),
    path("profile/delete-avatar/", views.delete_avatar, name="delete_avatar"),
    path("profile/update/", views.update_profile, name="update_profile"),
    path("personal-calendar.html", views.personal_calendar, name="personal_calendar"),
    path("profile/create-family/", views.create_family, name="create_family"),
]