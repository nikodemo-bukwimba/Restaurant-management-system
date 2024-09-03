# Generated by Django 5.0.3 on 2024-09-03 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oda', '0004_alter_order_ceo_remove_manager_user_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={},
        ),
        migrations.RemoveIndex(
            model_name='order',
            name='oda_order_created_7a7804_idx',
        ),
        migrations.RemoveField(
            model_name='order',
            name='ceo',
        ),
        migrations.RemoveField(
            model_name='order',
            name='manager',
        ),
        migrations.RemoveField(
            model_name='order',
            name='waiter',
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Cash'), ('credit_card', 'Credit Card'), ('phone', 'Phone')], default='cash', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
