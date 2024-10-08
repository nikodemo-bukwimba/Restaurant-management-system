# Generated by Django 5.0.3 on 2024-09-01 09:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'menu category',
                'verbose_name_plural': 'menu categories',
                'ordering': ['name'],
                'indexes': [models.Index(fields=['name'], name='orders_menu_name_e4d472_idx')],
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='menu_items/%Y/%m/%d')),
                ('description', models.TextField(blank=True)),
                ('customer_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('staff_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('available', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='orders.menucategory')),
            ],
            options={
                'ordering': ['name'],
                'indexes': [models.Index(fields=['id', 'slug'], name='orders_menu_id_234f5b_idx'), models.Index(fields=['name'], name='orders_menu_name_74ab71_idx'), models.Index(fields=['-created'], name='orders_menu_created_cc9b8e_idx')],
            },
        ),
    ]
