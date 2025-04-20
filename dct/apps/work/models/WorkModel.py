from django.db import models
from apps.work.models.admins.WorkModelAdmin import WorkModelAdmin
# from apps.work.models.consts import WorkStatusChoice
from config.constants import NULLABLE


class Work(models.Model):
    ModelAdmin = WorkModelAdmin

    name = models.CharField(verbose_name='Название',
                            max_length=100,
                            default='')
    description = models.CharField(verbose_name='Описание',
                                   max_length=255,
                                   **NULLABLE)
    car = models.ForeignKey('car.Car',
                            verbose_name='Машина',
                            on_delete=models.SET_NULL,
                            related_name='car_works',
                            **NULLABLE)
    price = models.PositiveIntegerField(verbose_name='Цена услуги')
    # status = models.PositiveIntegerField(
    #     verbose_name="Статус",
    #     choices=WorkStatusChoice.choices,
    #     default=WorkStatusChoice.none)

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'

    def __str__(self):
        return f'{self.name} {self.car}'
