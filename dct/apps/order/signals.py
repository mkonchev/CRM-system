from django.db.models.signals import pre_save
from apps.order.models.OrderModel import Order


def auto_fill_owner_id(instance, sender, **kwargs):
    if instance.car and (not instance.owner or instance.owner
                         != instance.car.owner):
        instance.owner = instance.car.owner


pre_save.connect(auto_fill_owner_id, sender=Order)
