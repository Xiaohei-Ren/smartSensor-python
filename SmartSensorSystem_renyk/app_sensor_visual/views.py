from django.http import JsonResponse
from django.shortcuts import render
from app_sensor_manage.models import Sensor
from app_user import forms as user_form
from app_dashboard import views as dashboard_views


# Create your views here. todo：报警记录

def sensor_detail(request, id):
    """
    根据id加载传感器详细页面
    :param request:
    :param id:
    :return:
    """
    login_form = user_form.UserForm()
    if not request.session.get('is_login', None):
        message = '未登录，请登录！'
        return render(request, 'user_login.html', locals())
    sensor = Sensor.objects.get(id=id, delete=0)
    # 设置全局变量
    id = int(id)
    global g_id
    g_id = id
    global g_name
    g_name = sensor.sensor_id
    global g_unit
    g_unit = sensor.unit
    # 获取实时传感器数据
    (time_list_res, value_list_res) = dashboard_views.data_reader(id)
    if not value_list_res == []:
        data_now = value_list_res[-1]
    return render(request, 'sensor_detail.html', locals())


g_id = 0
g_name = ""
g_unit = ""


def return_id_vl(request):
    (value_list, time_list) = dashboard_views.data_reader_all(g_id)
    return JsonResponse(value_list, safe=False)


def return_id_tl(request):
    (value_list, time_list) = dashboard_views.data_reader_all(g_id)
    return JsonResponse(time_list, safe=False)


def return_id_v(request):
    (value, time) = dashboard_views.data_reader(g_id)
    return JsonResponse(value, safe=False)


def return_id_t(request):
    (value, time) = dashboard_views.data_reader(g_id)
    return JsonResponse(time, safe=False)
