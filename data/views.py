from uuid import uuid4

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.contrib.auth import login, logout, authenticate
from .helper import send_forget_password


# Create your views here.


def register(request):
    try:
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                if User.objects.filter(username=username).first():
                    messages.success(request, 'username is taken')
                    return redirect('/register/')
                if User.objects.filter(email=email).first():
                    messages.success(request, 'email is taken')
                    return redirect('/register/')
                user_obj = User(first_name=first_name, last_name=last_name, email=email, username=username)
                user_obj.set_password(password)
                user_obj.save()
                profile = Profile.objects.create(user=user_obj)
                profile.save()
                return redirect('/login/')
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    return render(request, 'register.html')


def user_login(request):
    try:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username or not password:
                messages.success(request, "both username and password is required")
                return redirect('/login/')
            user_obj = User.objects.filter(username=username).first()
            if user_obj is None:
                messages.success(request, "user not found")
                return redirect('/login/')
            user = authenticate(username=username, password=password)
            if user is None:
                messages.success(request, "wrong password")
                return redirect('/login/')
            login(request, user)
            return redirect('index/', {'name': username})
    except Exception as e:
        print(e)
    return render(request, 'login.html')


def index(request):
    try:
        if request.method == "POST":
            logout(request)
            return redirect('/login/')

    except Exception as e:
        print(e)
    return render(request, 'index.html')


def forget_password(request):
    try:
        if request.method == "POST":
            username = request.POST.get('username')
            if not User.objects.filter(username=username).first():
                messages.success(request, 'not user found')
                return redirect('/forget/')
            user_obj = User.objects.get(username=username)
            print(user_obj.email)
            profile_obj = Profile.objects.get(user_id=user_obj)
            print(profile_obj)
            token = str(uuid4())
            print(token)
            print(type(token))
            profile_obj.forget_password_token = token
            profile_obj.save()
            print(profile_obj.forget_password_token)
            send_forget_password(user_obj.email, token)
            messages.success(request, 'email is send')

            return redirect('/forget/')
    except Exception as e:
        print(e)
    return render(request, 'forget.html')


def change_password(request, token):
    content = {}
    try:
        profile_obj = Profile.objects.filter(forget_password_token=token).first()
    except Exception as e:
        print(e)
    return render(request, 'change_password.html')
