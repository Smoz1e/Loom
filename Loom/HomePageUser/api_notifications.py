from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Notification
from pytz import timezone as pytz_timezone

@login_required
def get_notifications(request):
    ekb_tz = pytz_timezone('Asia/Yekaterinburg')
    now = timezone.now().astimezone(ekb_tz)
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False,
        task__date__lte=now.date(),
        task__start_time__lte=now.time()
    ).order_by('-created_at')[:20]
    data = []
    for notif in notifications:
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
        data.append(notif_data)
    return JsonResponse({'notifications': data})
