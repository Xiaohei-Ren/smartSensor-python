# Generated by Django 3.1.3 on 2020-12-07 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0011_currentuser_logout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currentuser',
            name='logout',
        ),
        migrations.AddField(
            model_name='currentuser',
            name='login',
            field=models.BooleanField(default=0, verbose_name='登出'),
        ),
    ]
