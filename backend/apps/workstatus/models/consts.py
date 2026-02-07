from django.db import models


class WorkStatusChoice(models.IntegerChoices):
    none = 0, 'Не начата'
    in_progress = 1, 'В работе'
    done = 2, 'Готово'
