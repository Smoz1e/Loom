from django.db import models
from django.contrib.auth.models import User

class PersonalTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='personal_tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    # Новые поля для модального окна:
    category = models.CharField(max_length=50, blank=True)  # тема/категория задачи
    is_private = models.BooleanField(default=False)  # приватность
    timezone = models.CharField(max_length=20, blank=True)  # часовой пояс
    repeat_type = models.CharField(max_length=20, blank=True)  # тип повтора: daily, monthly, yearly
    repeat_days = models.CharField(max_length=50, blank=True)  # повтор по дням недели (например, 'Пн,Вт')
    participants = models.TextField(blank=True)  # список участников (строкой, можно хранить через запятую)
    priority = models.CharField(max_length=10, blank=True, default='normal')  # low, normal, high
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.date} {self.start_time}-{self.end_time})"
