from django.shortcuts import render

def Register(request):
    return render(request, "register.html")

def Login(request):
    return render(request, "login.html")

# Create your views here.
