from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"id": "username", "required": ""}),
            "email": forms.EmailInput(attrs={"id": "email", "required": ""}),
            "password1": forms.PasswordInput(
                attrs={"id": "password", "required": "", "minlength": 8}
            ),
        }
    
