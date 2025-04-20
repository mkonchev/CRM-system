from django.db import models
from apps.workstatus.models.admins.WorkstatusModelAdmin import (
    WorkstatusModelAdmin)
from apps.workstatus.models.consts import WorkStatusChoice
from config.constants import NULLABLE


class Workstatus(models.Model):
    ModelAdmin = WorkstatusModelAdmin

    work = models.ForeignKey('work.Work',
                             verbose_name='Работа',
                             on_delete=models.CASCADE,
                             related_name='work_name',
                             **NULLABLE)
    order = models.ForeignKey('order.Order',
                              verbose_name='Заявка',
                              on_delete=models.CASCADE,
                              related_name='order_works',
                              **NULLABLE)
    status = models.PositiveIntegerField(
        verbose_name="Статус",
        choices=WorkStatusChoice.choices,
        default=WorkStatusChoice.none,
        )

    class Meta:
        verbose_name = 'Статус работы'
        verbose_name_plural = 'Статусы работ'

    def __str__(self):
        return f'{self.work} ({self.get_status_display()})'
