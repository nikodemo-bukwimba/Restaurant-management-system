# Generated by Django 5.0.3 on 2024-09-04 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oda', '0005_alter_order_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='sender_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
