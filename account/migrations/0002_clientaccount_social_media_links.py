# Generated by Django 5.0.1 on 2024-01-24 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientaccount',
            name='social_media_links',
            field=models.URLField(blank=True, max_length=250, null=True),
        ),
    ]
