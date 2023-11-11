from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        unique=True
    )
    email_verify = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' # Строка, описывающая имя поля в модели пользователя, которое используется в качестве уникального идентификатора, по-умолчанию это username
    REQUIRED_FIELDS = ['username'] # Список имен полей, которые будут запрашиваться при создании пользователя
