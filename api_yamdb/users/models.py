from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user',
        MODERATOR = 'moderator',
        ADMIN = 'admin',

    email = models.EmailField(
        _('email address'),
        max_length=254,
        unique=True,
        help_text=_(
            'Required. 254 characters or fewer. '
            'Letters, digits and @/./- only.'),
        validators=[validate_email],
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    bio = models.TextField(_('About'), blank=True)
    role = models.CharField(
        _('Choose a role'),
        choices=Role.choices,
        default=Role.USER,
        max_length=128,
    )
