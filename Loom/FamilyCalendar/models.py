from django.db import models
from RegAndAuth.models import Family
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from RegAndAuth.models import FamilyMember, Profile
from HomePageUser.models import Notification, PersonalTask

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

@receiver(post_save, sender=FamilyTask)
def create_family_task_notifications(sender, instance, created, **kwargs):
    if created:
        from RegAndAuth.models import FamilyMember
        from HomePageUser.models import Notification
        family_members = FamilyMember.objects.filter(family=instance.family)
        for member in family_members:
            profile = getattr(member, 'profile', None)
            user = getattr(profile, 'user', None) if profile else None
            print(f'Создаём уведомление для: {user}')  # Для отладки
            if user:
                try:
                    # Корректно формируем время для строки
                    if hasattr(instance.start_time, 'strftime'):
                        time_str = instance.start_time.strftime('%H:%M')
                    else:
                        time_str = str(instance.start_time)
                    Notification.objects.create(
                        user=user,
                        message=f'Напоминание: семейная задача "{instance.title}" будет в {time_str}',
                        family_task=instance,
                        is_read=False,
                        type='family'
                    )
                    print(f'Уведомление успешно создано для: {user}')
                except Exception as e:
                    print(f'Ошибка создания уведомления для {user}: {e}')
