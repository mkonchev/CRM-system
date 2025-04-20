from django.db import models
from apps.order.models.admins.OrderModelAdmin import OrderModelAdmin
from config.constants import NULLABLE


class Order(models.Model):
    ModelAdmin = OrderModelAdmin
    # list_display = ["owner", "car", "services", "checkpoints", "worker"]
    owner = models.ForeignKey('core.User',
                              verbose_name='Владелец',
                              on_delete=models.CASCADE,
                              related_name='order_owner',
                              help_text='Автозаполнение при выборе машины',
                              **NULLABLE)
    # Нужно поменять owner related_name
    car = models.ForeignKey('car.Car',
                            verbose_name='Машина',
                            on_delete=models.CASCADE,
                            related_name='orders')
    worker = models.ForeignKey('core.User',
                               verbose_name='Работник',
                               on_delete=models.CASCADE,
                               related_name='orders',
                               limit_choices_to={'is_active': True,
                                                 'role': 1})
    start_date = models.DateTimeField(verbose_name='Начало работ',
                                      auto_now=True)
    end_date = models.DateTimeField(verbose_name='Окончание работ', **NULLABLE)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'{self.owner} {self.car} {self.worker}'
