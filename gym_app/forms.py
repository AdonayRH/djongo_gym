from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Rutina


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2']

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class SimpleRutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la rutina'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la rutina'
            })
        }

        def clean_name(self):
            name = self.cleaned_data['name']
            if len(name) < 3:
                raise forms.ValidationError("El nombre ha de tener al menos tres caracteres")
            return name