from django.urls import path
from . import views
from . import api_delete_family_task, api_mark_family_task_completed

urlpatterns = [
    path('family-calendar/', views.family_calendar, name='family_calendar'),
    path('shared-calendar/', views.shared_calendar, name='shared_calendar'),
    path('api/delete_family_task/', api_delete_family_task.api_delete_family_task, name='api_delete_family_task'),
    path('api/mark_family_task_completed/', api_mark_family_task_completed.api_mark_family_task_completed, name='api_mark_family_task_completed'),
]
