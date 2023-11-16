# register/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Zmień 'home' na nazwę widoku strony głównej
    else:
        form = UserCreationForm()
    return render(request, 'register/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Zmień 'home' na nazwę widoku strony głównej
    else:
        form = AuthenticationForm()
    return render(request, 'register/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/register/login')  # Zmień 'home' na nazwę widoku strony głównej
