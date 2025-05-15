from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import timedelta
import calendar
from RegAndAuth.models import Profile
from .models import FamilyTask
import calendar as pycal
from collections import defaultdict

@login_required
def family_calendar(request):
    profile = Profile.objects.get(user=request.user)
    if not profile.family:
        return redirect('profile')
    # --- AJAX POST обработка создания семейной задачи ---
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        category = request.POST.get('category', '')
        timezone_val = request.POST.get('timezone', '')
        is_private = request.POST.get('is_private') == 'true'
        repeat_type = request.POST.get('repeat_type', '')
        repeat_days = request.POST.get('repeat_days', '')
        participants = request.POST.get('participants', '')
        priority = request.POST.get('priority', 'normal')
        errors = []
        if not title:
            errors.append('Название обязательно')
        if not date:
            errors.append('Дата обязательна')
        if not start_time or not end_time:
            errors.append('Время обязательно')
        if errors:
            return JsonResponse({'success': False, 'errors': errors})
        try:
            task = FamilyTask.objects.create(
                family=profile.family,
                title=title,
                description=description,
                date=date,
                start_time=start_time,
                end_time=end_time,
                category=category,
                timezone=timezone_val,
                is_private=is_private,
                repeat_type=repeat_type,
                repeat_days=repeat_days,
                participants=participants,
                priority=priority,
                created_by=request.user
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'errors': [str(e)]})
    today = timezone.localdate()
    date_str = request.GET.get('date')
    month_param = request.GET.get('month')
    year_param = request.GET.get('year')
    if date_str:
        try:
            current_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        except Exception:
            current_date = today
    else:
        current_date = today
    # Мини-календарь: месяц и год
    if month_param and year_param:
        try:
            month = int(month_param)
            year = int(year_param)
        except ValueError:
            month = current_date.month
            year = current_date.year
    else:
        month = current_date.month
        year = current_date.year
    prev_date = current_date - timedelta(days=1)
    next_date = current_date + timedelta(days=1)
    start_of_week = current_date - timedelta(days=current_date.weekday())
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
    week_days = [calendar.day_name[d.weekday()] for d in week_dates]
    hours = list(range(7, 24))
    # Мини-календарь: дни месяца
    first_day_of_month = timezone.datetime(year, month, 1).date()
    last_day_of_month = timezone.datetime(year, month, pycal.monthrange(year, month)[1]).date()
    month_days = [first_day_of_month + timedelta(days=i) for i in range((last_day_of_month - first_day_of_month).days + 1)]
    first_weekday = first_day_of_month.weekday()  # 0=Пн
    # Задачи для мини-календаря
    month_tasks = FamilyTask.objects.filter(family=profile.family, date__gte=first_day_of_month, date__lte=last_day_of_month)
    tasks_by_month_date = defaultdict(list)
    for task in month_tasks:
        tasks_by_month_date[task.date].append(task)
    # --- Основной календарь: задачи по дням недели ---
    week_tasks = FamilyTask.objects.filter(family=profile.family, date__in=week_dates).order_by('start_time')
    tasks_by_date = defaultdict(list)
    for task in week_tasks:
        tasks_by_date[task.date].append(task)
    # Для стрелок: предыдущий и следующий месяц
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    # Для красивого названия месяца
    RU_MONTHS = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
        7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
    }
    month_name = RU_MONTHS.get(month, str(month))
    context = {
        'current_date': current_date,
        'prev_date': prev_date,
        'next_date': next_date,
        'week_dates': week_dates,
        'week_days': week_days,
        'hours': hours,
        'family': profile.family,
        'month_days': month_days,
        'first_weekday': first_weekday,
        'tasks_by_month_date': tasks_by_month_date,
        'tasks_by_date': tasks_by_date,
        'month': month,
        'year': year,
        'month_name': month_name,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
    }
    return render(request, 'family-calendar.html', context)

# Create your views here.
