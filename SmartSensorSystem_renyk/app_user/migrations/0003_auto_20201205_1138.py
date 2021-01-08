# Generated by Django 3.1.3 on 2020-12-05 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0002_auto_20201204_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_no',
            field=models.CharField(default=10001, max_length=128, unique=True, verbose_name='用户编号'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login_time',
            field=models.DateTimeField(verbose_name='最近登录时间'),
        ),
    ]
