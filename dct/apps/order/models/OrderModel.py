from django.db import models
from apps.order.models.admins.OrderModelAdmin import OrderModelAdmin
from config.constants import NULLABLE


class Order(models.Model):
    ModelAdmin = OrderModelAdmin
    # list_display = ["owner", "car", "services", "checkpoints", "worker"]
    owner = models.ForeignKey('core.User',
                              verbose_name='ID владельца',
                              on_delete=models.CASCADE,
                              related_name='order_owner',
                              **NULLABLE)
    # Нужно поменять owner related_name
    car = models.ForeignKey('car.Car',
                            verbose_name='ID машины',
                            on_delete=models.CASCADE,
                            related_name='orders')
    worker = models.ForeignKey('core.User',
                               verbose_name='ID работника',
                               on_delete=models.CASCADE,
                               related_name='orders')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'{self.owner} {self.car} {self.worker}'
