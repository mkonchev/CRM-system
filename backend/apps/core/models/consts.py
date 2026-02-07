from django.db import models


class UserRoleChoice(models.IntegerChoices):
    admin = 0, 'Administrator'
    worker = 1, 'Worker'
    user = 2, 'User'
