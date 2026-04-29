from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from apps.work.models.WorkModel import Work


def clear_cache(sender, **kwargs):
    cache.delete("grouped_works")


post_delete.connect(clear_cache, sender=Work)
post_save.connect(clear_cache, sender=Work)
