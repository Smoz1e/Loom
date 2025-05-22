from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FamilyTask

@csrf_exempt
@require_POST
def api_mark_family_task_completed(request):
    task_id = request.POST.get('task_id')
    if not task_id:
        return JsonResponse({'success': False, 'error': 'No task_id provided'})
    try:
        task = FamilyTask.objects.get(id=task_id)
        task.is_completed = not task.is_completed
        task.save()
        return JsonResponse({'success': True, 'is_completed': task.is_completed})
    except FamilyTask.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task not found'})
