# Generated by Django 3.1.3 on 2020-12-07 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0009_currentuser_update_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_no',
        ),
    ]
