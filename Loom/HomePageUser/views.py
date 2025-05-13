from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from RegAndAuth.models import Profile
from datetime import datetime, timedelta
from collections import defaultdict
from .models import PersonalTask
import calendar

RU_MONTHS = {
    1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
    7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
}

@login_required
def HomePageUser(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def upload_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        profile = Profile.objects.get(user=request.user)
        profile.avatar = request.FILES['avatar']
        profile.save()
        messages.success(request, 'Аватарка успешно загружена!')
    return redirect('profile')

@login_required
def delete_avatar(request):
    profile = Profile.objects.get(user=request.user)
    if profile.avatar:
        profile.avatar.delete()
        profile.save()
        messages.success(request, 'Аватарка успешно удалена!')
    return redirect('profile')

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        profile = Profile.objects.get(user=user)

        # Обновление имени, фамилии и отчества
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        profile.bio = request.POST.get('middle_name', profile.bio)

        # Сохранение изменений
        user.save()
        profile.save()

        messages.success(request, 'Профиль успешно обновлен!')
        return redirect('profile')

@login_required
def personal_calendar(request):
    profile = Profile.objects.get(user=request.user)
    date_str = request.GET.get('date')
    month_param = request.GET.get('month')
    year_param = request.GET.get('year')
    # Определяем выбранную дату для основной сетки
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = datetime.today().date()
    else:
        selected_date = datetime.today().date()

    # Для мини-календаря: если передан месяц/год — используем их, иначе берём из выбранной даты
    if month_param and year_param:
        try:
            month = int(month_param)
            year = int(year_param)
        except ValueError:
            month = selected_date.month
            year = selected_date.year
    else:
        month = selected_date.month
        year = selected_date.year

    # Для основной сетки — неделя вокруг selected_date
    start_of_week = selected_date - timedelta(days=selected_date.weekday())
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
    prev_date = selected_date - timedelta(days=1)
    next_date = selected_date + timedelta(days=1)
    week_tasks = PersonalTask.objects.filter(user=request.user, date__in=week_dates).order_by('start_time')
    tasks_by_date = defaultdict(list)
    for task in week_tasks:
        tasks_by_date[task.date].append(task)

    # --- Мини-календарь ---
    first_day_of_month = datetime(year, month, 1).date()
    last_day_of_month = datetime(year, month, calendar.monthrange(year, month)[1]).date()
    month_days = [first_day_of_month + timedelta(days=i) for i in range((last_day_of_month - first_day_of_month).days + 1)]
    first_weekday = first_day_of_month.weekday()  # 0=Пн
    month_tasks = PersonalTask.objects.filter(user=request.user, date__gte=first_day_of_month, date__lte=last_day_of_month)
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
    month_name = RU_MONTHS.get(month, str(month))

    hours = range(7, 24)
    context = {
        'profile': profile,
        'selected_date': selected_date,
        'prev_date': prev_date,
        'next_date': next_date,
        'week_dates': week_dates,
        'tasks_by_date': tasks_by_date,
        'today': datetime.today().date(),
        'hours': hours,
        # Для мини-календаря:
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
    return render(request, 'personal-calendar.html', context)
