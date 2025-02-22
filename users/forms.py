from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


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
