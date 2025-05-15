from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta
import calendar
from RegAndAuth.models import Profile

@login_required
def family_calendar(request):
    profile = Profile.objects.get(user=request.user)
    if not profile.family:
        return redirect('profile')  # или на страницу с предложением создать/вступить в семью
    today = timezone.localdate()
    date_str = request.GET.get('date')
    if date_str:
        try:
            current_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        except Exception:
            current_date = today
    else:
        current_date = today
    prev_date = current_date - timedelta(days=1)
    next_date = current_date + timedelta(days=1)
    start_of_week = current_date - timedelta(days=current_date.weekday())
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
    week_days = [calendar.day_name[d.weekday()] for d in week_dates]
    hours = list(range(7, 24))
    context = {
        'current_date': current_date,
        'prev_date': prev_date,
        'next_date': next_date,
        'week_dates': week_dates,
        'week_days': week_days,
        'hours': hours,
        'family': profile.family,
    }
    return render(request, 'family-calendar.html', context)

# Create your views here.
