from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user',
        MODERATOR = 'moderator',
        ADMIN = 'admin',

    email = models.EmailField(
        'email address',
        max_length=254,
        unique=True,
        help_text=(
            'Required. 254 characters or fewer. '
            'Letters, digits and @/./- only.'),
        validators=[validate_email],
        error_messages={
            'unique': "A user with that email already exists.",
        },
    )

    bio = models.TextField('About', blank=True)
    role = models.CharField(
        'Choose a role',
        choices=Role.choices,
        default=Role.USER,
        max_length=128,
    )
