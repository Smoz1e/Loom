from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Notification
from pytz import timezone as pytz_timezone
from FamilyCalendar.models import FamilyTask

@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')[:20]
    ekb_tz = pytz_timezone('Asia/Yekaterinburg')
    now = timezone.now().astimezone(ekb_tz)
    filtered = []
    for notif in notifications:
        # Для персональных задач
        if notif.task and notif.task.date <= now.date() and notif.task.start_time <= now.time():
            filtered.append(notif)
        # Для семейных задач
        elif notif.family_task:
            ft = notif.family_task
            if ft.date <= now.date() and ft.start_time <= now.time():
                filtered.append(notif)
    data = []
    for notif in filtered:
        notif_data = {
            'id': notif.id,
            'message': notif.message,
            'created_at': notif.created_at.astimezone(ekb_tz).strftime('%Y-%m-%d %H:%M:%S'),
            'is_read': notif.is_read,
        }
        if notif.task:
            notif_data['task'] = {
                'id': notif.task.id,
                'title': notif.task.title,
                'date': notif.task.date.strftime('%Y-%m-%d'),
                'start_time': notif.task.start_time.strftime('%H:%M'),
            }
        if notif.family_task:
            ft = notif.family_task
            notif_data['family_task'] = {
                'id': ft.id,
                'title': ft.title,
                'date': ft.date.strftime('%Y-%m-%d'),
                'start_time': ft.start_time.strftime('%H:%M'),
            }
        data.append(notif_data)
    return JsonResponse({'notifications': data})
