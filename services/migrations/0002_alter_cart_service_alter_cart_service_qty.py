# Generated by Django 5.0.1 on 2024-01-27 14:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service', to='services.service'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='service_qty',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
    ]