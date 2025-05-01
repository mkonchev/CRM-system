from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.managers.UserManager import UserManager
from config.constants import NULLABLE
from apps.core.models.consts import UserRoleChoice


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        null=True,
        blank=True,
    )
    phone_number = models.CharField(
        verbose_name='Phone Number',
        max_length=12,
        default='-',
    )
    tg_login = models.CharField(
        verbose_name='Login in Telegramm',
        **NULLABLE,
        max_length=200,
    )
    email = models.EmailField(_('email address'), unique=True)
    role = models.PositiveIntegerField(
        verbose_name='Role in system',
        choices=UserRoleChoice.choices,
        default=UserRoleChoice.user,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
