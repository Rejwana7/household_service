# Generated by Django 5.0.1 on 2024-03-06 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_alter_clientaccount_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientaccount',
            name='profile_image',
            field=models.ImageField(default='default_pic.jpg', null=True, upload_to='account/media/uploads'),
        ),
    ]