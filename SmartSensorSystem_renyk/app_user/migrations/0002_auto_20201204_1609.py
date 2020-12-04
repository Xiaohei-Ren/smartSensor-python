# Generated by Django 3.1.3 on 2020-12-04 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login_time',
            field=models.DateTimeField(blank=True, verbose_name='最近登录时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(max_length=256, verbose_name='角色权限'),
        ),
    ]
