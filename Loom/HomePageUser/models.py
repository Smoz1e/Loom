from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    is_completed = models.BooleanField(default=False)  # выполнена ли задача

    def __str__(self):
        return f"{self.title} ({self.date} {self.start_time}-{self.end_time})"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    task = models.ForeignKey('PersonalTask', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    family_task = models.ForeignKey('FamilyCalendar.FamilyTask', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')

    TYPE_CHOICES = [
        ('personal', 'Личное'),
        ('family', 'Семейное'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='personal')
    accepted = models.BooleanField(null=True, blank=True, default=None)  # None - не отвечал, True - принял, False - отклонил

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:30]}"

@receiver(post_save, sender=PersonalTask)
def create_notification_for_task(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            message=f'Напоминание: задача "{instance.title}" будет в {instance.start_time.strftime("%H:%M")}',
            task=instance,
            is_read=False,
            type='personal'
        )
