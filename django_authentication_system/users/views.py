from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ValidationError

from .forms import UserCreationForm, AuthenticationForm
from .utils import send_email_for_verify


User = get_user_model()

class MyLoginView(LoginView):
    form_class = AuthenticationForm


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm # from .forms
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid(): 
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(email=email, password=password) # получение созданного user
            send_email_for_verify(request, user)
            return redirect('confirm_email')
        else:
            context = {
               'form': form
            }
            return render(request, self.template_name, context)
        

class EmailVerify(View):

    def get(self, request, uidb64, token): 
        user = self.get_user(uidb64)
        if (user is not None) and (default_token_generator.check_token(user, token)): # в случае, если пользователь получен и токен корректный, то...
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return redirect('invalid_verify')


    # эта функция сопоставляет uid и токен из ссылки с данными на сервере и, если все хорошо, возвращает пользователя. Так как метод не использует self, его можно сделать статическим
    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user