from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, SimpleRutinaForm


def register(request):
    """
    Maneja el registro de nuevos usuarios.

    Si la solicitud es POST, intenta registrar al usuario con los datos enviados.
    Si el registro es exitoso, el usuario es autenticado e inicia sesión automáticamente.
    Si hay errores en el formulario, muestra un mensaje de error.

    Args:
        request (HttpRequest): Objeto que representa la solicitud HTTP actual.

    Returns:
        HttpResponse: Renderiza la plantilla 'register.html' con el formulario.
    """
    if request.method == 'POST':
        # Crear formulario de registro con los datos enviados
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo usuario en la base de datos
            user = form.save()
            # Iniciar sesión automáticamente después del registro
            login(request, user)
            messages.success(request, 'Register complete sussefuly')
            # Redirigir al usuario a la página principal
            return redirect('home')
        else:
            messages.error(request, 'Error doing the register. Please fix the errors')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    """
    Maneja el inicio de sesión de usuarios.

    Si la solicitud es POST, verifica las credenciales del usuario. 
    Si son válidas, inicia sesión y redirige al usuario a la página principal.
    Si las credenciales son incorrectas, muestra un mensaje de error.

    Args:
        request (HttpRequest): Objeto que representa la solicitud HTTP actual.

    Returns:
        HttpResponse: Renderiza la plantilla 'login.html' con el formulario.
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user = get_user_model().objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    messages.success(request, 'Conexión exitosa')
                    return redirect('home')
            except get_user_model().DoesNotExist:
                messages.error(request, 'Claves de acceso incorrectas')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})
    
@login_required
def home(request):
    """
    Renderiza la página principal de la aplicación.

    Esta vista requiere que el usuario haya iniciado sesión.

    Args:
        request (HttpRequest): Objeto que representa la solicitud HTTP actual.

    Returns:
        HttpResponse: Renderiza la plantilla 'home.html'.
    """
    return render(request, 'home.html', {'show_messages': True})

def logout_view(request):
    """
    Cierra la sesión del usuario actual.

    Después de cerrar sesión, redirige al usuario a la página principal.

    Args:
        request (HttpRequest): Objeto que representa la solicitud HTTP actual.

    Returns:
        HttpResponseRedirect: Redirige a la página principal ('home').
    """
    logout(request)
    return redirect('home')

def crear_rutinas(request):
    """
    Maneja la creación de nuevas rutinas.

    Si la solicitud es POST, intenta guardar la rutina en la base de datos.
    Si es válida, redirige al usuario a la lista de rutinas.
    Si no es válida, renderiza nuevamente el formulario con errores.

    Args:
        request (HttpRequest): Objeto que representa la solicitud HTTP actual.

    Returns:
        HttpResponse: Renderiza la plantilla 'crear_rutina.html' con el formulario.
    """
    if request.method == 'POST':
        form = SimpleRutinaForm(request.POST)
        if form.is_valid():
            rutina = form.save()
            return redirect('rutina_list')
    else:
        form = SimpleRutinaForm()
    return render(request, 'crear_rutina.html', {'form': form})