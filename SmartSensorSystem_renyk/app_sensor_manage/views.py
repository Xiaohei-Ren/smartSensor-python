import datetime
import re
from django.http import JsonResponse
from django.shortcuts import render, redirect
from app_sensor_manage import forms as sensor_from
from app_sensor_manage.models import Sensor
from app_user import forms as user_form

# Create your views here.

def add(request):
    """
    新增传感器 todo：增加下拉选框改进
    :param request: 
    :return: 
    """
    # 判断是否登录
    login_form = user_form.UserForm()
    if not request.session.get('is_login', None):
        message = '未登录，请登录！'
        return render(request, 'user_login.html', locals())
    if request.method == "POST":
        add_form = sensor_from.SensorAddForm(request.POST)
        message = "请检查填写的内容！"
        if add_form.is_valid():
            sensor_id = add_form.cleaned_data.get("sensor_id")
            sensor_name = add_form.cleaned_data.get("name")
            sensor_sort = add_form.cleaned_data.get("sort")
            sensor_location = add_form.cleaned_data.get("location")
            comment = add_form.cleaned_data.get("comment")
            unit = ""
            if sensor_sort == '温度传感器':
                unit = "℃"
            elif sensor_sort == '压力传感器':
                unit = "Mpa"
            elif sensor_sort == '流量传感器':
                unit = "m³/h"
            elif sensor_sort == '浓度传感器':
                unit = "ppm"
            elif sensor_sort == '智能电表':
                unit = ""
            # 参数校验
            same_sensor_id = Sensor.objects.filter(sensor_id=sensor_id)
            if same_sensor_id:
                message = "传感器ID已存在"
                return render(request, 'sensor_add.html', locals())
            same_sensor_name = Sensor.objects.filter(name=sensor_name)
            if same_sensor_name:
                message = "传感器名称已存在"
                return render(request, 'sensor_add.html', locals())
                # 传感器id校验
            res = re.match("^[A-Za-z0-9]+$", sensor_id)  # 只能输入数字+字母ID
            if not res:
                message = "传感器ID格式错误"
                return render(request, 'sensor_add.html', locals())
            # 传感器名称校验
            res = re.match('^[0-9\u4e00-\u9fa5]*$', sensor_name)  # 只能输入汉字+数字
            if not res:
                message = "传感器名称格式错误"
                return render(request, 'sensor_add.html', locals())
            new_sensor = Sensor()
            new_sensor.sensor_id = sensor_id
            new_sensor.name = sensor_name
            new_sensor.sort = sensor_sort
            new_sensor.location = sensor_location
            new_sensor.comment = comment
            new_sensor.create_time = datetime.datetime.now()
            new_sensor.unit = unit
            new_sensor.save()
            message = "添加成功！"
            return redirect('/sensor_list/')
        else:
            message = "字段不能为空!"
            return render(request, 'sensor_add.html', locals())
    else:
        add_form = sensor_from.SensorAddForm()
        return render(request, 'sensor_add.html', locals())


def sensor_list(request):
    """
    传感器列表
    :param request: 
    :return: 
    """
    list_sensor = Sensor.objects.all()
    return render(request, 'sensor_list.html', locals())


def temp_sensor_list(request):
    list_sensor = Sensor.objects.filter(sort='温度传感器')
    return render(request, 'sensor_list_temp.html', locals())


def pre_sensor_list(request):
    list_sensor = Sensor.objects.filter(sort='压力传感器')
    return render(request, 'sensor_list_pre.html', locals())


def flow_sensor_list(request):
    list_sensor = Sensor.objects.filter(sort='流量传感器')
    return render(request, 'sensor_list_flow.html', locals())


def con_sensor_list(request):
    list_sensor = Sensor.objects.filter(sort='浓度传感器')
    return render(request, 'sensor_list_con.html', locals())


def ele_sensor_list(request):
    list_sensor = Sensor.objects.filter(sort='智能电表')
    return render(request, 'sensor_list_ele.html', locals())


def test(request):
    """
    js返回用户信息
    :param request:
    :return:
    """
    name = '访客用户'
    try:
        name = request.session['user_name']
    finally:
        return JsonResponse(name, safe=False)


