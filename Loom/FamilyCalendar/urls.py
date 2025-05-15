from django.urls import path
from . import views

urlpatterns = [
    path('family-calendar/', views.family_calendar, name='family_calendar'),
]
