from django.db import models
from RegAndAuth.models import Family
from django.contrib.auth.models import User

# Create your models here.

class FamilyTask(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    category = models.CharField(max_length=50, blank=True)
    timezone = models.CharField(max_length=20, blank=True)
    repeat_type = models.CharField(max_length=20, blank=True)
    repeat_days = models.CharField(max_length=50, blank=True)
    participants = models.TextField(blank=True)  # список участников (строкой, можно хранить через запятую)
    priority = models.CharField(max_length=10, blank=True, default='normal')
    is_private = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)  # выполнена ли задача
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_family_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.date} {self.start_time}-{self.end_time})"
