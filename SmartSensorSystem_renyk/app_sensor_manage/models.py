from django.db import models


# Create your models here.

class Sensor(models.Model):
    id = models.BigAutoField('id', unique=True, primary_key=True)  # id 主键
    sensor_id = models.CharField('传感器id', max_length=128, )  # 传感器id
    name = models.CharField('名称', max_length=128, )  # 名称
    station_id = models.CharField('加氢站编号', max_length=128)  # 所在站编号
    station_name = models.CharField('加氢站名称', max_length=128)  # 所在站名称
    sort = models.CharField('传感器类别', max_length=128)  # 类别（温度、气压、氢气浓度、功率、电量等传感器）
    location = models.CharField('所在位置', max_length=128)  # 位置
    info = models.CharField('详细信息', max_length=128, blank=True)  # 详细信息
    status = models.CharField('当前状态', max_length=128, blank=True)  # 状态（正常、故障、检修）
    create_time = models.DateTimeField('创建时间')  # 创建时间
    last_update_time = models.DateTimeField('修改时间', auto_now=True)  # 最后修改时间
    comment = models.CharField('备注', max_length=128, blank=True)  # 备注
    delete = models.BooleanField('删除', default=0)  # 逻辑删除


class Station(models.Model):
    id = models.AutoField('id', unique=True, primary_key=True)  # id 主键
    station_id = models.CharField('加氢站编号', max_length=128, unique=True)  # 站id
    name = models.CharField('加氢站名称', max_length=128, unique=True)  # 站名
    address = models.CharField('地址', max_length=128)  # 地址
    status = models.CharField('当前状态', max_length=128, blank=True)  # 状态
    delete = models.BooleanField('删除', default=0)  # 逻辑删除


class SensorRecord(models.Model):
    id = models.AutoField('id', unique=True, primary_key=True)  # id 主键
    sensor_id = models.CharField('传感器id', max_length=128, )  # 传感器id
    user_no = models.CharField('用户编号', max_length=128, null=True)  # 用户编号
    update_time = models.DateTimeField('修改时间', auto_now=True)  # 修改时间
    operate = models.IntegerField('操作类型', max_length=128)  # 操作类型(1新增 2修改 3删除)
