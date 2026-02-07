from django.db.models.signals import post_save
from apps.workstatus.models.WorkstatusModel import Workstatus
from apps.workstatus.models.consts import WorkStatusChoice


def update_order_completion_status_signal(sender, instance, **kwargs):
    order = instance.order
    all_works = order.items.all()

    order.is_completed = all_works.exists() and all(
        work.status == WorkStatusChoice.done
        for work in all_works
    )
    order.save(update_fields=['is_completed'])


post_save.connect(
    update_order_completion_status_signal,
    sender=Workstatus,
)
