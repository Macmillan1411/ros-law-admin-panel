from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Имя")
    last_name = forms.CharField(required=True, label="Фамилия")
    patronymic = forms.CharField(required=False, label="Отчество")
    position = forms.CharField(required=True, label="Должность")
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "patronymic",
            "position",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

        self.fields["username"].label = "Имя пользователя"
        self.fields["password"].label = "Пароль"
