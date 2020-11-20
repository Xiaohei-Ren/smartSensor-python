from django.db import models

# Create your models here.


class User(models.Model):

    gender = (
        ('admin', "管理员"),
        ('user', "用户"),
    )

    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    email = models.CharField(unique=True, max_length=256)
    phone_number = models.CharField(unique=True, max_length=256)
    role = models.CharField(choices=gender, default="用户", max_length=256)
    create_time = models.DateTimeField()
    last_login_time = models.DateTimeField()



