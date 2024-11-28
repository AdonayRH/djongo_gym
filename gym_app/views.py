from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
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
            try:
                user = get_user_model().objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    messages.success(request, 'Session successful')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid password')
            except get_user_model().DoesNotExist:
                messages.error(request, 'Invalid email address')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})
    
# home
@login_required
def home(request):
    return render(request, 'home.html')

# log_out
def logout_view(request):
    logout(request)
    return redirect('home')