from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification
from FamilyCalendar.models import FamilyTask
import json
from datetime import datetime

@login_required
@require_POST
def api_respond_family_notification(request):
    try:
        data = json.loads(request.body)
        notif_id = int(data.get('id'))
        accepted = data.get('accepted')
        if accepted not in [True, False, 'true', 'false', 1, 0, '1', '0']:
            return JsonResponse({'success': False, 'error': 'Некорректный ответ'})
        accepted_bool = True if accepted in [True, 'true', 1, '1'] else False
    except Exception:
        return JsonResponse({'success': False, 'error': 'Некорректные данные запроса'})
    try:
        notif = Notification.objects.get(id=notif_id, user=request.user, type='family')
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Уведомление не найдено'})
    notif.accepted = accepted_bool
    notif.save(update_fields=['accepted'])
    # Если пользователь принял задачу, создаём напоминание сразу, но помечаем его как is_read=True, если время ещё не наступило
    if accepted_bool and notif.family_task:
        task_date = notif.family_task.date
        task_time = notif.family_task.start_time
        now_date = datetime.now().date()
        now_time = datetime.now().time()
        already_exists = Notification.objects.filter(user=request.user, family_task=notif.family_task, type='reminder').exists()
        if not already_exists:
            is_read = False
            if (task_date > now_date) or (task_date == now_date and task_time > now_time):
                is_read = True  # Скрытое напоминание, появится когда наступит время
            Notification.objects.create(
                user=request.user,
                message=f'Напоминание: семейная задача "{notif.family_task.title}" будет в {notif.family_task.start_time.strftime("%H:%M")}',
                family_task=notif.family_task,
                is_read=is_read,
                type='reminder'
            )
    return JsonResponse({'success': True, 'accepted': notif.accepted})
