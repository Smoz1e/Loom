from django.contrib import admin
from .models import PersonalTask, Notification
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class PersonalTaskInline(admin.TabularInline):
    model = PersonalTask
    extra = 0

class NotificationInline(admin.TabularInline):
    model = Notification
    extra = 0

class UserAdmin(BaseUserAdmin):
    inlines = [PersonalTaskInline, NotificationInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(PersonalTask)
admin.site.register(Notification)
