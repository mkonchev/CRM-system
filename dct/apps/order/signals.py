from django.db.models.signals import pre_save, m2m_changed
from apps.order.models.OrderModel import Order
from apps.workstatus.models.WorkstatusModel import Workstatus
from apps.workstatus.models.consts import WorkStatusChoice


def auto_fill_owner_id(instance, sender, **kwargs):
    if instance.car and (not instance.owner or instance.owner
                         != instance.car.owner):
        instance.owner = instance.car.owner


# def create_workstatuses_for_order_items(sender, instance, action, **kwargs):
#     if action == "post_add":
#         Workstatus.objects.filter(order=instance).delete()
#         Workstatus.objects.bulk_create([
#             Workstatus(
#                 work=work,
#                 order=instance,
#                 status=WorkStatusChoice.none
#             )
#             for work in instance.works.all()
#         ])
# def update_order_completion_status(sender, instance, **kwargs):
#     order = instance.order
#     all_works = order.items.all()
#     if not all_works.exists():
#         order.is_completed = False
#         order.save(update_fields=['is_completed'])
#         return
#     all_completed = not any(
#         work.status != WorkStatusChoice.completed
#         for work in all_works
#     )
#     if order.is_completed != all_completed:
#         order.is_completed = all_completed
#         order.save(update_fields=['is_completed'])


# m2m_changed.connect(update_order_completion_status,
#                     sender=Workstatus)
pre_save.connect(auto_fill_owner_id, sender=Order)
