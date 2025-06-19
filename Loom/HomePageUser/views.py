from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from RegAndAuth.models import Profile, Family, FamilyMember
from datetime import datetime, timedelta
from collections import defaultdict
from .models import PersonalTask
from FamilyCalendar.models import FamilyTask
from .api_respond_family_notification import api_respond_family_notification
import calendar
import random
import string

RU_MONTHS = {
    1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
    7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
}

@login_required
def HomePageUser(request):
    profile = Profile.objects.get(user=request.user)
    is_admin = False
    if profile.family:
        from RegAndAuth.models import FamilyMember
        try:
            is_admin = FamilyMember.objects.get(family=profile.family, profile=profile).is_admin
        except FamilyMember.DoesNotExist:
            is_admin = False
    return render(request, 'profile.html', {'profile': profile, 'is_admin': is_admin})

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
        # --- Сохраняем email ---
        user.email = request.POST.get('email', user.email)

        # Сохранение изменений
        user.save()
        profile.save()

        messages.success(request, 'Профиль успешно обновлен!')
        return redirect('profile')

@login_required
def personal_calendar(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        # Получаем данные из POST (AJAX или обычный POST)
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        date_str = request.POST.get('date', '')
        start_time_str = request.POST.get('start_time', '')
        end_time_str = request.POST.get('end_time', '')
        category = request.POST.get('category', '').strip()
        is_private = request.POST.get('is_private', 'false') == 'true'
        timezone = request.POST.get('timezone', '').strip()
        repeat_type = request.POST.get('repeat_type', '').strip()
        repeat_days = request.POST.get('repeat_days', '').strip()
        participants = request.POST.get('participants', '').strip()
        priority = request.POST.get('priority', 'normal')

        # Валидация (минимальная)
        errors = []
        if not title:
            errors.append('Название обязательно')
        if not date_str:
            errors.append('Дата обязательна')
        if not start_time_str or not end_time_str:
            errors.append('Время обязательно')
        try:
            # Поддержка формата 'YYYY-MM-DD' (HTML5 <input type="date">)
            if '-' in date_str:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            else:
                date = datetime.strptime(date_str, '%d.%m.%Y').date()
        except Exception:
            errors.append('Некорректная дата')
            date = None
        try:
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
        except Exception:
            errors.append('Некорректное время')
            start_time = end_time = None
        # Проверка пересечений с личными и семейными задачами (полное пересечение по времени)
        if start_time and end_time and date:
            # Личные задачи
            personal_overlaps = PersonalTask.objects.filter(
                user=request.user,
                date=date
            ).exclude(
                end_time__lte=start_time
            ).exclude(
                start_time__gte=end_time
            )
            # Семейные задачи
            family_overlaps = FamilyTask.objects.filter(
                family=profile.family,
                date=date
            ).exclude(
                end_time__lte=start_time
            ).exclude(
                start_time__gte=end_time
            )
            if personal_overlaps.exists() or family_overlaps.exists():
                errors.append('Время задачи пересекается с другой задачей в календаре!')
        if errors:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': errors})
            else:
                messages.error(request, '\n'.join(errors))
                return redirect('personal_calendar')
        # Сохраняем задачу
        PersonalTask.objects.create(
            user=request.user,
            title=title,
            description=description,
            date=date,
            start_time=start_time,
            end_time=end_time,
            category=category,
            is_private=is_private,
            timezone=timezone,
            repeat_type=repeat_type,
            repeat_days=repeat_days,
            participants=participants,
            priority=priority
        )
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('personal_calendar')

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

def generate_family_code(length=8):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

@login_required
def create_family(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        if profile.family:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'У вас уже есть семья. Нельзя создать вторую.'})
            messages.error(request, 'У вас уже есть семья. Нельзя создать вторую.')
            return redirect('profile')
        family_name = request.POST.get('family_name', '').strip()
        if not family_name:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Введите название семьи!'})
            messages.error(request, 'Введите название семьи!')
            return redirect('profile')
        # Генерируем уникальный код
        for _ in range(10):
            code = generate_family_code()
            if not Family.objects.filter(code=code).exists():
                break
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Не удалось создать уникальный код семьи. Попробуйте еще раз.'})
            messages.error(request, 'Не удалось создать уникальный код семьи. Попробуйте еще раз.')
            return redirect('profile')
        family = Family.objects.create(name=family_name, code=code)
        profile.family = family
        profile.save()
        FamilyMember.objects.create(family=family, profile=profile, is_admin=True)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'family_name': family.name, 'family_code': family.code})
        messages.success(request, f'Семья "{family_name}" создана! Код: {code}')
    return redirect('profile')

@login_required
def join_family(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        if profile.family:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Вы уже состоите в семье. Сначала покиньте текущую.'})
            from django.contrib import messages
            messages.error(request, 'Вы уже состоите в семье. Сначала покиньте текущую.')
            return redirect('profile')
        code = request.POST.get('join_family_code', '').strip().upper()
        from RegAndAuth.models import Family
        try:
            family = Family.objects.get(code=code)
        except Family.DoesNotExist:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Семья с таким кодом не найдена.'})
            from django.contrib import messages
            messages.error(request, 'Семья с таким кодом не найдена.')
            return redirect('profile')
        profile.family = family
        profile.save()
        from RegAndAuth.models import FamilyMember
        FamilyMember.objects.create(family=family, profile=profile, is_admin=False)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'family_name': family.name, 'family_code': family.code})
        from django.contrib import messages
        messages.success(request, f'Вы присоединились к семье: {family.name}')
    return redirect('profile')

@login_required
@require_POST
def remove_family_member(request):
    import json
    profile = Profile.objects.get(user=request.user)
    if not profile.family:
        return JsonResponse({'success': False, 'error': 'Нет семьи'})
    try:
        data = json.loads(request.body)
        user_id = int(data.get('user_id'))
    except Exception:
        return JsonResponse({'success': False, 'error': 'Некорректные данные'})
    # Проверка: только админ может удалять
    is_admin = FamilyMember.objects.filter(family=profile.family, profile=profile, is_admin=True).exists()
    if not is_admin:
        return JsonResponse({'success': False, 'error': 'Только администратор семьи может удалять участников'})
    # Нельзя удалить себя
    if user_id == request.user.id:
        return JsonResponse({'success': False, 'error': 'Нельзя удалить себя'})
    # Удаляем участника
    try:
        member = FamilyMember.objects.get(family=profile.family, profile__user__id=user_id)
        member.profile.family = None
        member.profile.save()
        member.delete()
        return JsonResponse({'success': True})
    except FamilyMember.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Пользователь не найден в семье'})

@login_required
def family_members_ajax(request):
    profile = Profile.objects.get(user=request.user)
    if not profile.family:
        return JsonResponse({'success': True, 'members': []})
    members = profile.family.members.select_related('profile__user').all()
    def get_avatar_url(p):
        if p.avatar:
            return p.avatar.url
        return None
    members_data = [
        {
            'id': m.profile.user.id,
            'name': f"{m.profile.user.first_name} {m.profile.user.last_name}".strip() or m.profile.user.username,
            'avatar': get_avatar_url(m.profile)
        }
        for m in members
    ]
    return JsonResponse({'success': True, 'members': members_data})

@login_required
@require_POST
def leave_family(request):
    profile = Profile.objects.get(user=request.user)
    if not profile.family:
        return JsonResponse({'success': False, 'error': 'Вы не состоите в семье'})
    family = profile.family  # Сохраняем ссылку до отвязки
    # Удаляем пользователя из FamilyMember и отвязываем семью
    FamilyMember.objects.filter(family=family, profile=profile).delete()
    profile.family = None
    profile.save()
    # Если после выхода не осталось участников, удаляем семью
    if not FamilyMember.objects.filter(family=family).exists():
        family.delete()
    return JsonResponse({'success': True})
