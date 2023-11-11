from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm,
    AuthenticationForm as DjangoAuthenticationForm
)  
from django.core.exceptions import ValidationError
from django import forms

from .utils import send_email_for_verify


User = get_user_model() # возвращает значение AUTH_USER_MODEL из settings.py

class AuthenticationForm(DjangoAuthenticationForm):

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if not self.user_cache.email_verify: # в случае, если email не верифицирован, то пользователю на почту снова отправляется письмо для верификации 
                send_email_for_verify(self.request, self.user_cache)
                raise ValidationError(
                    'Имейл не верифицирован! Проверьте вашу почту',
                    code="inactive",
                )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data



class UserCreationForm(DjangoUserCreationForm): 
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )
    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ('username', 'email')