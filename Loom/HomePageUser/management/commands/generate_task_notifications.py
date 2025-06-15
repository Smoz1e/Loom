from django.core.management.base import BaseCommand
from django.utils import timezone
from HomePageUser.models import PersonalTask, Notification
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Создает уведомления для задач, которые должны начаться сейчас.'

    def handle(self, *args, **kwargs):
        now = timezone.localtime()
        today = now.date()
        current_time = now.time().replace(second=0, microsecond=0)
        tasks = PersonalTask.objects.filter(date=today, start_time=current_time, is_completed=False)
        for task in tasks:
            # Проверяем, есть ли уже уведомление для этой задачи и пользователя
            if not Notification.objects.filter(user=task.user, task=task, message__icontains='начинается', created_at__date=today, created_at__hour=now.hour, created_at__minute=now.minute).exists():
                Notification.objects.create(
                    user=task.user,
                    message=f'Напоминание: задача "{task.title}" начинается сейчас!',
                    task=task
                )
                self.stdout.write(self.style.SUCCESS(f'Уведомление создано для пользователя {task.user} и задачи {task.title}'))
