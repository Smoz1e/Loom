from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Profile
from django.http import JsonResponse
import random
import json
from .sms_utils import send_sms


def send_sms_code(request):
    if request.method == "POST":
        data = json.loads(request.body)
        phone = data.get("phone")
        if not phone:
            return JsonResponse({"message": "Номер телефона не указан!"}, status=400)
        code = str(random.randint(10000, 99999))
        request.session['sms_code'] = code
        request.session['sms_phone'] = phone
        send_sms(phone, code)
        return JsonResponse({"message": "Код отправлен на номер!"})
    return JsonResponse({"message": "Неверный метод!"}, status=405)


def Register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        phone = request.POST.get("phone")
        role = request.POST.get("role")
        sms_code = request.POST.get("sms_code")

        if password != confirm_password:
            messages.error(request, "Пароли не совпадают!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Имя пользователя уже занято!")
            return redirect("register")

        if Profile.objects.filter(phone=phone).exists():
            messages.error(request, "Номер телефона уже зарегистрирован!")
            return redirect("register")

        # Проверка SMS-кода
        session_code = request.session.get('sms_code')
        session_phone = request.session.get('sms_phone')
        if not session_code or not session_phone or phone != session_phone or sms_code != session_code:
            messages.error(request, "Неверный или просроченный код подтверждения!")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password)
        # Если имя не указано явно, копируем username в first_name
        user.first_name = username
        user.save()
        Profile.objects.create(user=user, phone=phone, role=role)
        messages.success(request, "Регистрация прошла успешно! Войдите в систему.")
        # Очищаем код после успешной регистрации
        request.session.pop('sms_code', None)
        request.session.pop('sms_phone', None)
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
