# Generated by Django 5.0.3 on 2024-09-05 10:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oda', '0007_order_manager_confirmed'),
        ('users', '0002_waiter_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='waiter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.waiter'),
        ),
    ]
