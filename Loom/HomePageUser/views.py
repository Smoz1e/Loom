from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from RegAndAuth.models import Profile
from datetime import datetime, timedelta
from collections import defaultdict
from .models import PersonalTask
import calendar

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
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = datetime.today().date()
    else:
        selected_date = datetime.today().date()

    # Определяем начало недели (понедельник)
    start_of_week = selected_date - timedelta(days=selected_date.weekday())
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]

    # Для навигации по дням
    prev_date = selected_date - timedelta(days=1)
    next_date = selected_date + timedelta(days=1)

    # Все задачи пользователя за неделю
    week_tasks = PersonalTask.objects.filter(user=request.user, date__in=week_dates).order_by('start_time')
    # Группируем задачи по дате
    tasks_by_date = defaultdict(list)
    for task in week_tasks:
        tasks_by_date[task.date].append(task)

    # --- Мини-календарь ---
    year = selected_date.year
    month = selected_date.month
    first_day_of_month = datetime(year, month, 1).date()
    last_day_of_month = datetime(year, month, calendar.monthrange(year, month)[1]).date()
    # Список всех дней месяца
    month_days = [first_day_of_month + timedelta(days=i) for i in range((last_day_of_month - first_day_of_month).days + 1)]
    # Для сетки: сколько дней в неделе до первого дня месяца (чтобы правильно выровнять)
    first_weekday = first_day_of_month.weekday()  # 0=Пн
    # Задачи пользователя за месяц
    month_tasks = PersonalTask.objects.filter(user=request.user, date__gte=first_day_of_month, date__lte=last_day_of_month)
    tasks_by_month_date = defaultdict(list)
    for task in month_tasks:
        tasks_by_month_date[task.date].append(task)

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
    }
    return render(request, 'personal-calendar.html', context)
