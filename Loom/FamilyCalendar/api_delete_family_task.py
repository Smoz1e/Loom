from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import FamilyTask

@csrf_protect
@require_POST
def api_delete_family_task(request):
    task_id = request.POST.get('task_id')
    if not task_id:
        return JsonResponse({'success': False, 'error': 'No task_id provided'})
    try:
        task = FamilyTask.objects.get(id=task_id)
        task.delete()
        return JsonResponse({'success': True})
    except FamilyTask.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task not found'})
