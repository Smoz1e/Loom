"""
URL configuration for Loom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('RegAndAuth.urls')),  # Подключение маршрутов из приложения RegAndAuth
]
