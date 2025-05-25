from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from RegAndAuth.views import *
from . import api_delete_personal_task
from . import api_mark_personal_task_completed

urlpatterns = [
    path("profile/", views.HomePageUser, name="profile"),
    path("profile/upload-avatar/", views.upload_avatar, name="upload_avatar"),
    path("profile/delete-avatar/", views.delete_avatar, name="delete_avatar"),
    path("profile/update/", views.update_profile, name="update_profile"),
    path("personal-calendar.html", views.personal_calendar, name="personal_calendar"),
    path("profile/create-family/", views.create_family, name="create_family"),
    path("profile/join-family/", views.join_family, name="join_family"),
    path("profile/family-members/", views.family_members_ajax, name="family_members_ajax"),
    path("profile/remove-family-member/", views.remove_family_member, name="remove_family_member"),
    path("api/delete_personal_task/", api_delete_personal_task.api_delete_personal_task, name="api_delete_personal_task"),
    path("api/mark_personal_task_completed/", api_mark_personal_task_completed.api_mark_personal_task_completed, name="api_mark_personal_task_completed"),
    path("api/toggle_task_completion/", api_mark_personal_task_completed.api_mark_personal_task_completed, name="toggle_task_completion"),
    path("profile/leave-family/", views.leave_family, name="leave_family"),
]