from django.db import models

# Create your models here.


class User(models.Model):

    id = models.AutoField('id', unique=True, primary_key=True)
    name = models.CharField('用户名', max_length=256)
    password = models.CharField('密码', max_length=256)
    email = models.CharField('邮箱', unique=True, max_length=256)
    phone_number = models.CharField('电话', unique=True, max_length=256)
    role = models.CharField('角色权限', max_length=256)
    create_time = models.DateTimeField('创建时间')
    last_login_time = models.DateTimeField('最近登录时间', null=True)
    delete = models.BooleanField('删除', default=0)

    class Meta:
        ordering = ['-create_time']


class CurrentUser(models.Model):
    id = models.AutoField('id', unique=True, primary_key=True)
    user_no = models.CharField('用户编号', max_length=128, null=True)
    update_time = models.DateTimeField('登录时间')
    login = models.BooleanField('登出', default=0)
    logout = models.BooleanField('登出', default=0)

    class Meta:
        ordering = ['-update_time']
