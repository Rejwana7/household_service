# Generated by Django 5.0.1 on 2024-03-04 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_clientaccount_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientaccount',
            name='profile_image',
            field=models.ImageField(default='media/uploads/default.jpg', null=True, upload_to='account/media/uploads'),
        ),
    ]
