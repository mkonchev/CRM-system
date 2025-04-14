from django.db import models

from apps.car.models.admins.CarModelAdmin import CarModelAdmin


class Car(models.Model):
    ModelAdmin = CarModelAdmin

    number = models.CharField(verbose_name='Номер', max_length=10, default='')
    mark = models.CharField(verbose_name='Марка', max_length=50, default='')
    model = models.CharField(verbose_name='Модель', max_length=50, default='')
    vin = models.CharField(verbose_name='VIN/Номер кузова',
                           max_length=100,
                           default='')
    owner = models.ForeignKey('core.User',
                              verbose_name='ID владельца',
                              on_delete=models.CASCADE,
                              related_name='cars',
                              )

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

    def __str__(self):
        return f'{self.mark} {self.model} {self.vin}'
