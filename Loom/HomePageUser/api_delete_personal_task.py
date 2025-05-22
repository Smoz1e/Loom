from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import PersonalTask
import json

@login_required
@require_POST
def api_delete_personal_task(request):
    try:
        data = json.loads(request.body)
        task_id = int(data.get('id'))
    except Exception:
        return JsonResponse({'success': False, 'error': 'Некорректные данные запроса'})
    try:
        task = PersonalTask.objects.get(id=task_id, user=request.user)
    except PersonalTask.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Задача не найдена'})
    task.delete()
    return JsonResponse({'success': True})
