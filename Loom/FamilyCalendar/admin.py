from django.contrib import admin
from .models import FamilyTask

class FamilyTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'start_time', 'family')

admin.site.register(FamilyTask, FamilyTaskAdmin)
