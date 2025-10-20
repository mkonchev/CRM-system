from django.db.models.signals import pre_save, post_save
from apps.order.models.OrderModel import Order
from apps.order.tasks import send_workstatus_complete_email


def auto_fill_owner_id(instance, sender, **kwargs):
    if instance.car and (not instance.owner or instance.owner
                         != instance.car.owner):
        instance.owner = instance.car.owner


def send_email_if_is_complete(instance, sender, **kwargs):
    if instance.is_completed:
        send_workstatus_complete_email.delay(
            instance.owner.email,
            str(instance.car),
            str(instance.total_price())
        )


pre_save.connect(auto_fill_owner_id, sender=Order)
post_save.connect(send_email_if_is_complete, sender=Order)
