from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from users.models import CustomUser
from users.forms import CustomRegisterForm, CustomLoginForm


def register_view(request):
    if request.method == "POST":
        form_user = CustomRegisterForm(request.POST, request.FILES)
        if form_user.is_valid():
            form_user.save()
            return redirect('/login/')
    else:
        form_user = CustomRegisterForm()
    return render(request, 'users/register.html', {'form': form_user})


def auth_login_view(request):
    if request.method == "POST":
        form_user = CustomLoginForm(data=request.POST)
        if form_user.is_valid():
            user = form_user.get_user()
            login(request, user)
            return redirect('/profile/')
    else:
        form_user = CustomLoginForm()
    return render(request, 'users/login.html', {'form': form_user})


def auth_logout_view(request):
    logout(request)
    return redirect('/login/')


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, 'users/profile.html', {'user': user})