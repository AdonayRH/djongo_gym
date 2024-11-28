from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm

# Register
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Register complete sussefuly')
            return redirect('home')
        else:
            messages.error(request, 'Error doing the register. Please fix the errors')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# Login
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Session sussecful')
                return redirect('home')
            else:
                messages.error(request, 'Email o password error')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form':form})
    
# home
@login_required
def home(request):
    return render(request, 'home.html')

# log_out
def logout_view(request):
    logout(request)
    return redirect('home')