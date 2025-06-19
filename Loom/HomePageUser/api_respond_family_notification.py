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
        comment = data.get('comment', None)  # Получаем комментарий, если он есть

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
    if not accepted_bool and comment:
        notif.message += f' Причина отклонения: {comment}'  # Добавляем комментарий к уведомлению
    notif.save(update_fields=['accepted', 'message'])

    # Если пользователь принял задачу, создаём напоминание
    if accepted_bool and notif.family_task:
        now = datetime.now().date(), datetime.now().time()
        task_date = notif.family_task.date
        task_time = notif.family_task.start_time
        if (task_date < datetime.now().date()) or (task_date == datetime.now().date() and task_time <= datetime.now().time()):
            if not Notification.objects.filter(user=request.user, family_task=notif.family_task, type='reminder').exists():
                Notification.objects.create(
                    user=request.user,
                    message=f'Напоминание: семейная задача "{notif.family_task.title}" будет в {notif.family_task.start_time.strftime("%H:%M")}',
                    family_task=notif.family_task,
                    is_read=False,
                    type='reminder'
                )
    # --- Новое: уведомление создателю задачи о принятии ---
    if notif.family_task and notif.family_task.created_by and accepted_bool:
        creator = notif.family_task.created_by
        if creator != request.user:
            Notification.objects.create(
                user=creator,
                message=f'{request.user.get_full_name() or request.user.username} принял(а) семейную задачу "{notif.family_task.title}"',
                family_task=notif.family_task,
                is_read=False,
                type='info'  # Новый тип для информационных уведомлений
            )

    return JsonResponse({'success': True, 'accepted': notif.accepted})
