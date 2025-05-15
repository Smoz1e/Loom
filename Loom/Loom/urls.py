from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('login')),  # Перенаправление на страницу авторизации
    path('', include('RegAndAuth.urls')),
    path('', include('HomePageUser.urls')),
    path('', include('FamilyCalendar.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)