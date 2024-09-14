# Generated by Django 5.1.1 on 2024-09-14 09:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_expense_reported'),
        ('users', '0009_remove_report_end_time_remove_report_report_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='shift',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.shift'),
        ),
    ]
