# Generated by Django 5.0.3 on 2025-04-30 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_remove_order_works_remove_order_workstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name='Готовность'),
        ),
    ]
