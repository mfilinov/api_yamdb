from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Админ'

    email = models.EmailField(
        'email address',
        max_length=254,
        unique=True,
        help_text=(
            'Required. 254 characters or fewer. '
            'Letters, digits and @/./- only.'),
        validators=[validate_email],
        error_messages={
            'unique': 'Пользователь с таким email уже существует.',
        },
    )

    bio = models.TextField('О себе', blank=True)
    role = models.CharField(
        'Выберите роль',
        choices=Role.choices,
        default=Role.USER,
        max_length=128,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
