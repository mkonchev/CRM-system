from django.db import models

from apps.car.models.admins.CarModelAdmin import CarModelAdmin
from config.constants import NULLABLE


class Car(models.Model):
    ModelAdmin = CarModelAdmin

    number = models.CharField(verbose_name='Номер',
                              max_length=10,
                              default='',
                              **NULLABLE)
    mark = models.CharField(verbose_name='Марка', max_length=50, default='')
    model = models.CharField(verbose_name='Модель', max_length=50, default='')
    vin = models.CharField(verbose_name='VIN/Номер кузова',
                           max_length=100,
                           default='')
    year = models.PositiveIntegerField(verbose_name='Год выпуска', **NULLABLE)
    owner = models.ForeignKey('core.User',
                              verbose_name='ID владельца',
                              on_delete=models.SET_NULL,
                              related_name='car_owner',
                              **NULLABLE
                              )

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

    def __str__(self):
        return f'{self.mark} {self.model} {self.year}'
