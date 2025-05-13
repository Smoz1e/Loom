from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from RegAndAuth.models import Profile

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
    return render(request, 'personal-calendar.html', {'profile': profile})
