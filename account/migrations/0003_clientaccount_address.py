# Generated by Django 5.0.1 on 2024-01-27 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_clientaccount_social_media_links'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientaccount',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]