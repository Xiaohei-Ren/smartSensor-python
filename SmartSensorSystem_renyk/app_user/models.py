from django.db import models

# Create your models here.


class User(models.Model):

    id = models.AutoField('id', unique=True, primary_key=True)
    name = models.CharField('用户名', max_length=128)
    password = models.CharField('密码', max_length=128)
    email = models.CharField('邮箱', unique=True, max_length=128)
    phone_number = models.CharField('电话', unique=True, max_length=128)
    role = models.CharField('角色权限', max_length=128)
    create_time = models.DateTimeField('创建时间')
    last_login_time = models.DateTimeField('最近登录时间', null=True)
    delete = models.BooleanField('删除', default=0)

    class Meta:
        ordering = ['-create_time']