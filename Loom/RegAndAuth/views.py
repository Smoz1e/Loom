from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Profile


def Register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        phone = request.POST.get("phone")
        role = request.POST.get("role")

        if password != confirm_password:
            messages.error(request, "Пароли не совпадают!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Имя пользователя уже занято!")
            return redirect("register")

        if Profile.objects.filter(phone=phone).exists():
            messages.error(request, "Номер телефона уже зарегистрирован!")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, phone=phone, role=role)
        messages.success(request, "Регистрация прошла успешно! Войдите в систему.")
        return redirect("login")

    return render(request, "register.html")

def Login(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        try:
            profile = Profile.objects.get(phone=phone)
            user = authenticate(request, username=profile.user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect("profile")  # Перенаправление на личный кабинет
            else:
                messages.error(request, "Неверный номер телефона или пароль!")
        except Profile.DoesNotExist:
            messages.error(request, "Пользователь с таким номером телефона не найден!")

        return redirect("login")

    return render(request, "login.html")

def Dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "")
