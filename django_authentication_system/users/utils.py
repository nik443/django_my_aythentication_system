from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def send_email_for_verify(request, user):
    current_site = get_current_site(request)
    context = {
        "user": user,
        "domain": current_site.domain, # получение домена
        "uid": urlsafe_base64_encode(force_bytes(user.pk)), # кодируем id пользователя в байтовую строку, которую вставим в ссылку на подтверждение почты
        "token": default_token_generator.make_token(user), # закодированный токен, который будем сопоставлять с uid и проверять не изменялась ли ссылка
    }
    message = render_to_string(template_name='registration/verify_email.html', context=context) # render_to_string - передает в шаблон контекст, рендерит его и возвращает строкой
    email = EmailMessage(
        'Verify email', # заголовок
        message, # само письмо
        to=[user.email] # кому отправится письмо
    )
    email.send() # оправка письма на email пользователя