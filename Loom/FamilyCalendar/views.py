from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
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
