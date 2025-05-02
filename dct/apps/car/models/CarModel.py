from django.db import models

from apps.car.models.admins.CarModelAdmin import CarModelAdmin
from apps.car.services.VINDecoder import VINDecoder
from config.constants import NULLABLE


class Car(models.Model):
    ModelAdmin = CarModelAdmin

    number = models.CharField(
        verbose_name='Номер',
        max_length=10,
        default='',
        **NULLABLE,
    )
    mark = models.CharField(
        verbose_name='Марка',
        max_length=50,
        default='',
        **NULLABLE,
    )
    model = models.CharField(
        verbose_name='Модель',
        max_length=50,
        default='',
        **NULLABLE,
    )
    vin = models.CharField(
        verbose_name='VIN/Номер кузова',
        max_length=100,
        default='',
        **NULLABLE,
    )
    year = models.PositiveIntegerField(verbose_name='Год выпуска', **NULLABLE)
    owner = models.ForeignKey(
        'core.User',
        verbose_name='ID владельца',
        on_delete=models.SET_NULL,
        related_name='car_owner',
        **NULLABLE,
    )

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

    def __str__(self):
        return f'{self.mark} {self.model} {self.year}'

    def save(self, *args, **kwargs):
        """Автоматически заполняем данные при сохранении"""
        if self.vin and not self.mark:
            vehicle_data = VINDecoder.get_vehicle_info(self.vin)
            if vehicle_data:
                self.mark = vehicle_data['mark']
                self.model = vehicle_data['model']
                self.year = vehicle_data['year']
        super().save(*args, **kwargs)
